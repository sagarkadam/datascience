# import requests
import json
import string
import random
import os

def callAPI(url, data):
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    return requests.post(url, data=data, headers=headers)


def creatCard():

    #create a disk with always a new name
    url = 'http://localhost:8080'
    disk_name = 'problemName' + str(random.randrange(0,10000)) + '_gce-nfs-disk'
    pvc_name = 'problemName' + str(random.randrange(0, 10000)) + '_pvc_pod'
    nfs_pod = 'problemName' + str(random.randrange(0,10000)) + '_nfs_pod'
    nfs_pod_service = 'problemName' + str(random.randrange(0,10000)) + '_nfs_pod_service'
    file_names = ['1nfs.json', '2nfs-service.json']

    value = 'gcloud compute disks create --size=10GB --zone=us-central1-a' + disk_name
    os.system(value)

    with open(file_names[0], 'r') as f:
        data = json.load(f)
        data['metadata']['name'] = nfs_pod
        data['spec']['template']['spec']['volumes'][0]['gcePersistentDisk']['pdName'] = disk_name
        data['spec']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = pvc_name
        data['spec']['template']['spec']['volumes'][0]['name'] = pvc_name
        #callAPI(url  + '/apis/apps/v1/namespace/default/deployments', data)

        print(data)

    with open(file_names[1], 'r') as f:
        data = json.load(f)
        data['metadata']['name'] = nfs_pod_service
        data['spec']['selector']['role'] = nfs_pod
        # results = callAPI(url  + '/api/v1/namespaces/default/services', data)

        print(data)

creatCard()