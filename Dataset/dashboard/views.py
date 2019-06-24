import json
from pprint import pprint
from itertools import chain

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic, View
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .documents import PostDocument
from .models import DatasetProfile, DataScienceFaq
from .serializer import DatasetProfileSerializer, dataset_review_serializer
# Create your views here.
import random
import os
from django.core.paginator import Paginator


class DatasetProfileList(APIView):

    def get(self, request):
        page = request.GET.get('page', 1)

        datasets = DatasetProfile.objects.filter(dataset_valid='success').values()

        paginator = Paginator(datasets, 10)

        page_data = paginator.page(page)

        return render(request,'dashboard/datasets.html',context={'all_datasets':page_data})


class IndexView(generic.ListView):
    template_name = 'dashboard/index.html'

    def get_queryset(self):
        return True


class DatasetsView(generic.ListView):
    template_name = 'dashboard/datasets.html'
    context_object_name = 'all_datasets'

    def get_queryset(self):
        return DatasetProfile.objects.all()


class AboutUsView(generic.ListView):
    template_name = 'dashboard/about_us.html'

    def get_queryset(self):
        return True


class DataScience_FAQ(APIView):

    def get(self, request):
        templateName = 'dashboard/datascience_faq.html'

        resultant_data = []
        datascience_faq_category = DataScienceFaq.objects.values('question_category').annotate(dcount=Count('question_category'))
        datascience_faq_category = [result for result in datascience_faq_category]
        datascience_faq_category = [result['question_category'] for result in datascience_faq_category]
        for value in datascience_faq_category:
            data = DataScienceFaq.objects.filter(question_category=value).order_by('id').values()[:3]
            data = [result for result in data]
            resultant_data.append(data)
        return render(request, template_name=templateName, context={'data': resultant_data})


class DataScience_FAQ_Url(UpdateAPIView):

    def get(self, request,faq_value):
        url = request.path.split('/')[2]
        questions_data = DataScienceFaq.objects.filter(question_url=url).order_by('id').values()
        return render(request, 'dashboard/datascience_faq.html', {'questions_data': questions_data})


class SubmitView(generic.ListView):
    template_name = 'dashboard/submit.html'
    return_template_name = 'dashboard/thanks.html'

    def post(self, request, *args, **kwargs):
        stuff = request.POST.get('problem_name')
        print(stuff)
        return render(request, self.return_template_name, {'stuff': stuff})

    def get_queryset(self):
        return True


class PrivacyView(generic.ListView):
    template_name = 'dashboard/privacy.html'

    def get_queryset(self):
        return True


class ThanksView(generic.ListView):
    template_name = 'dashboard/thanks.html'

    def get_queryset(self):
        return True


class DatasetCreate(CreateAPIView):
    template_name = 'dashboard/submit.html'

    def get_queryset(self):
        return True

    serializer_class = DatasetProfileSerializer

    def get(self,request):
        return render(request,self.template_name,{})

    def post(self, request, *args, **kwargs):
        problem_name = request.data['problem_name']
        max_algorithm=request.data['max_algorithm']
        model_accuracy = request.data['model_accuracy']
        file_type = request.data['file_type']
        dataset_size = request.data['dataset_size']
        document_link = request.data['document_link']
        github_link = request.data['github_link']
        dataset_zip = request.data['dataset_zip']
        jupyter_link = request.data['jupyter_link']
        username = request.data['user'] + str(random.randrange(0, 100000, 3))
        user = User.objects.create(username=username, email=request.data['email'])
        user.save()
        user_data = User.objects.filter(username=username).values('username', 'email', 'id')
        list_result = [value for value in user_data]
        item = DatasetProfile.objects.create(problem_name=problem_name,max_algorithm=max_algorithm,model_accuracy=model_accuracy,
                                             file_type=file_type,dataset_size=dataset_size,document_link=document_link,
                                             github_link=github_link,dataset_zip=dataset_zip, user_jupyter_link = jupyter_link,
                                             user_id=list_result[0]['id'],dataset_valid = 'pending')
        item.save()
        data = {
            'username':request.data['user'],
            'domain': request.META.get('HTTP_HOST'),  # current_site.domain,
        }

        message = render_to_string('dashboard/dataset_submit.html', data)
        mail_subject = 'Dataset submitted successfully !!!'  # mail subject
        to_email = request.data['email']  # mail id to be sent to
        email = EmailMessage(mail_subject, message,
                             to=[to_email])  # takes 3 args: 1. mail subject 2. message 3. mail id to send
        email.send()

        return render(request,'dashboard/thanks.html',{'user_data':user_data})


class Get_datasets(RetrieveAPIView):
    def get(self,request):
        datasets = DatasetProfile.objects.filter(~Q(dataset_valid=True)).values()
        return render(request,'dashboard/dashboard_panel.html',context={'all_datasets':datasets})


class dataset_review(UpdateAPIView):
    serializer_class =dataset_review_serializer
    queryset = DatasetProfile.objects.all()

    def get(self,request,pk):
        try:
            item=DatasetProfile.objects.get(id=pk)
            return render(request,'dashboard/dataset_review.html',context={'all_datasets':item, 'id':pk})
        except:
            return render(request,'dashboard/error_page.html',{})

    def post(self,request,pk):
        if request.POST['dataset_reivew_msg'] == 'success':
            message = "Dataset approved succesfully"
            mail_subject = "Dataset Approved"
            dataset_files = DatasetProfile.objects.filter(id=pk).values('dataset_zip', 'user_jupyter_link')
            # data_link = dataset_files[0]['dataset_zip']
            # jupyter_link = dataset_files[0]['user_jupyter_link']
            #
            # os.system('wget ' + data_link)
            # os.system('wget ' + jupyter_link)
            #
            # dataset_file_path = "/datasetstorvolume/website_datasets_files/" + str(pk)
            # code_file_path = "/home/ubuntu/testingjupyterdata/website_code_files/" + str(pk)
            # aws_url = 'http://13.233.212.57/notebook/notebooks/website_code_files/'
            #
            # jupyter_file_name = jupyter_link.split('/')[-1].replace('%20','\ ')
            # data_file_name = data_link.split('/')[-1]
            # jupyter_file_name_link = jupyter_link.split('/')[-1]
            #
            # os.system('ssh ubuntu@13.233.212.57 "mkdir "' + dataset_file_path)
            # os.system('ssh ubuntu@13.233.212.57 "mkdir "' + code_file_path)
            #
            # data_scp_copy = 'scp ' + data_file_name + ' ubuntu@13.233.212.57:' + dataset_file_path
            # jupyter_scp_copy = 'scp ' + jupyter_file_name + ' ubuntu@13.233.212.57:' + code_file_path
            #
            # os.system(data_scp_copy)
            # os.system(jupyter_scp_copy)
            # os.system('rm ' + data_file_name)
            # os.system('rm ' + jupyter_file_name)
            #
            # aws_jupyter_link = aws_url + str(pk) + '/' + jupyter_file_name_link
            DatasetProfile.objects.filter(id=pk).update(aws_jupyter_link="dasdad")
            DatasetProfile.objects.filter(id=pk).update(dataset_valid='success')

        else:
            DatasetProfile.objects.filter(id=pk).update(dataset_valid='error')
            message = request.POST['error_msg']
            mail_subject = 'Error Report for Submitted Dataset'  # mail subject

        user_id = DatasetProfile.objects.filter(id=pk).values('user_id')
        user_data = User.objects.filter(id=user_id[0]['user_id']).values('username', 'email')
        to_email = user_data[0]['email']  # mail id to be sent to
        email = EmailMessage(mail_subject, message,
                             to=[to_email])  # takes 3 args: 1. mail subject 2. message 3. mail id to send
        email.send()
        return render(request, 'dashboard/dashboard_panel.html', context={})


class AdminPanelView(UpdateAPIView):

    def get(self, request):
        templateName = 'dashboard/admin_panel.html'

        return render(request, template_name=templateName, context={})


class AdminPanelViewURl(UpdateAPIView):

    def get(self, request, url_value):
        url = request.path.split('/')[2]
        templateName = ''
        if url == 'dashboard_panel':
            templateName = 'dashboard/dashboard_panel.html'
        elif url == 'faq_panel':
            templateName = 'dashboard/faq_panel.html'
        elif url == 'datasets_panel':
            datasets = DatasetProfile.objects.filter(dataset_valid='pending').values()
            return render(request, 'dashboard/datasets_panel.html', context={'all_datasets': datasets})
        else:
            templateName = 'dashboard/admin_panel.html'

        return render(request, template_name=templateName, context={})

    def post(self, request, *args, **kwargs):
        url = request.path.split('/')[2]
        if url == 'faq_submit':
            question_title = request.data['question_title']
            answer = request.data['answer']
            question_category = request.data['question_category']
            question_url = question_category.split(' ')[0].lower() + '_' +  question_category.split(' ')[1].lower()
            data = DataScienceFaq.objects.create(question=question_title, answer=answer, question_category=question_category,
                                                 question_url=question_url)
            data.save()
            return render(request, template_name='dashboard/faq_panel.html', context={'question_save': True})
        else:
            res = {
                'message': 'Something bad happened',
                'data': {},
                'success': False
            }

            """ This method is used to log in user """

            try:
                if request.POST.get('username') and request.POST.get('password'):
                    username = request.POST.get('username')             # takes the username from request
                    password = request.POST.get('password')             # takes password from request .

                    user = authenticate(username=username, password=password)       # checks if username and password are available in DB.
                    if user:
                        if user.is_active:
                            login(request, user)
                            res['message']="Logged in Successfully"
                            res['success']=True
                            res['data'] =None
                            datasets = DatasetProfile.objects.filter(~Q(dataset_valid='pending')).values()
                            user_data = User.objects.filter().values('username', 'email')
                            from itertools import chain
                            a =  []
                            b = {}
                            for x in datasets:
                                for y in user_data:
                                    b.update(y)
                                    pass
                                a.append(b)

                            merged_queryset = [x for x in datasets] + [y for y in user_data]
                            print(a)
                            return render(request, 'dashboard/dashboard_panel.html', context={'all_datasets': datasets, 'user_data':user_data})
                        else:
                            res['message'] = "Your account was inactive."
                            return render(request, 'dashboard/admin_panel', context={'response': res})
                    else:
                        res['message'] = 'Username or Password is not correct' #Invalid login details
                        return render(request, 'dashboard/admin_panel', context={'response': res})
            except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
                print(e)
                return redirect(reverse('admin_panel'), permanent=True)


class datasets_panel(RetrieveAPIView):

    def get(self,request):
        datasets = DatasetProfile.objects.filter(dataset_valid='pending').values()
        print(datasets)
        return render(request, 'dashboard/datasets_panel.html', context={'all_datasets': datasets})

    def post(self, request, *args, **kwargs):

        res = {
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }

        """ This method is used to log in user """

        try:
            if request.POST.get('username') and request.POST.get('password'):
                username = request.POST.get('username')             # takes the username from request
                password = request.POST.get('password')             # takes password from request .

                user = authenticate(username=username, password=password)       # checks if username and password are available in DB.
                if user:
                    if user.is_active:
                        login(request, user)
                        res['message']="Logged in Successfully"
                        res['success']=True
                        res['data'] =None
                        datasets = DatasetProfile.objects.filter(~Q(dataset_valid='pending')).values()
                        user_data = User.objects.filter().values('username', 'email')
                        from itertools import chain
                        a =  []
                        b = {}
                        for x in datasets:
                            for y in user_data:
                                b.update(y)
                                pass
                            a.append(b)

                        merged_queryset = [x for x in datasets] + [y for y in user_data]
                        print(a)
                        return render(request, 'dashboard/dashboard_panel.html', context={'all_datasets': datasets, 'user_data':user_data})
                    else:
                        res['message'] = "Your account was inactive."
                        return render(request, 'dashboard/admin_panel', context={'response': res})
                else:
                    res['message'] = 'Username or Password is not correct' #Invalid login details
                    return render(request, 'dashboard/admin_panel', context={'response': res})
        except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)
            return redirect(reverse('admin_panel'), permanent=True)


class dashboard_panel(CreateAPIView):

    def get(self,request):
        datasets = DatasetProfile.objects.filter(dataset_valid='pending').values()

        return render(request, 'dashboard/dashboard_panel.html', context={'all_datasets': datasets})

    def post(self, request, *args, **kwargs):

        res = {
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }

        """ This method is used to log in user """

        try:
            if request.POST.get('username') and request.POST.get('password'):
                username = request.POST.get('username')             # takes the username from request
                password = request.POST.get('password')             # takes password from request .

                user = authenticate(username=username, password=password)       # checks if username and password are available in DB.
                if user:
                    if user.is_active:
                        login(request, user)
                        res['message']="Logged in Successfully"
                        res['success']=True
                        res['data'] =None
                        datasets = DatasetProfile.objects.filter(~Q(dataset_valid='pending')).values()
                        user_data = User.objects.filter().values('username', 'email')
                        from itertools import chain
                        a =  []
                        b = {}
                        for x in datasets:
                            for y in user_data:
                                b.update(y)
                                pass
                            a.append(b)

                        merged_queryset = [x for x in datasets] + [y for y in user_data]
                        print(a)
                        return render(request, 'dashboard/dashboard_panel.html', context={'all_datasets': datasets, 'user_data':user_data})
                    else:
                        res['message'] = "Your account was inactive."
                        return render(request, 'dashboard/admin_panel', context={'response': res})
                else:
                    res['message'] = 'Username or Password is not correct' #Invalid login details
                    return render(request, 'dashboard/admin_panel', context={'response': res})
        except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)
            return redirect(reverse('admin_panel'), permanent=True)


class filter_data(RetrieveAPIView):
    queryset = DatasetProfile.objects.all()

    def get(self,request):
        file_type_list = json.loads((request.GET['filter_data']))
        print(file_type_list)
        arguments = {}
        for k, v in file_type_list.items():
            if v:
                arguments[k] = ", ".join(v)
        data_items = DatasetProfile.objects.filter(**arguments).values()
        data_items = [result for result in data_items]
        return JsonResponse(data_items, safe=False)


class sort_data(RetrieveAPIView):

    def get(self,request):
        sort_data_list = request.GET['sort_data']
        value = ''
        if sort_data_list == 'newest_first':
            value = '-id'
        elif sort_data_list == 'accuracy_hl':
            value = '-model_accuracy'
        elif sort_data_list == 'accuracy_lh':
            value = 'model_accuracy'
        data = DatasetProfile.objects.all().order_by(value).values()
        data = [result for result in data]
        return JsonResponse(data, safe=False)


class search(RetrieveAPIView):

    queryset = DatasetProfile.objects.all()

    def get(self,request):

        search_text=request.GET.get('search_text')

        if search_text:
            search_objest=Search()
            search_response = search_objest.query("multi_match", query=search_text,  type='cross_fields',fields=['problem_name', 'max_algorithm','model_accuracy'])
            datasetes = [result for result in search_response]

        else:
            datasetes = 0

        return render(request, 'dashboard/datasets.html', context={'all_datasets': datasetes})


class ds_treasure(CreateAPIView):

    def get(self,request):

        return render(request, 'dashboard/ds_treasure.html', context={})


class ml_5w1h(CreateAPIView):

    def get(self,request):

        return render(request, 'dashboard/ml_5w1h.html', context={})

