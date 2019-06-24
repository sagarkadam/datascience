FROM python:3.6.7

COPY ./Dataset /usr/src/chatapp

# Copy the rest of the applicaion's code
COPY ./requirements.txt /usr/src/chatapp/

WORKDIR /usr/src/chatapp/

# Install dependencies
RUN pip3 install -r requirements.txt

EXPOSE 8000
# Run the app
COPY docker-script.sh /usr/src/chatapp/
CMD ["./docker-script.sh"]
