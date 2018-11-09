FROM fedora:latest

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt &&\
    pip3 install gunicorn

COPY . /app
EXPOSE 8080
CMD ["/usr/local/bin/gunicorn", "-w", "1", "che_marketplace_backend:create_app()", "-b", "0.0.0.0:8080"]
