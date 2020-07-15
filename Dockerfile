FROM tiangolo/uwsgi-nginx-flask:python3.8
ENV MODULE_NAME "init.create_app"

COPY requirements.txt requirements.txt

#COPY CowBook/Forms /app/Forms
#COPY CowBook/Models /app/Models
#COPY CowBook/templates /app/templates
#COPY CowBook/Util /app/Util
#COPY CowBook/Views /app/Views
#COPY CowBook/__init__.py /app/__init__.py
#COPY CowBook/api.py /app/api.py
#COPY CowBook/app.py /app/app.py
#COPY CowBook/default_settings.py app/default_settings.py
#COPY CowBook/init.py app/init.py
#COPY CowBook/routes.py /app/routes.py

#COPY CowBook/static/Assets /app/static/Assets
#COPY CowBook/static/Assets /app/static/Assets
COPY CowBook /app/CowBook
COPY uwsgi.ini /app/uwsgi.ini

RUN rm -r /app/CowBook/Data
RUN mkdir /app/CowBook/Data
RUN rm -r /app/CowBook/static/Pictures
RUN mkdir /app/CowBook/static/Pictures
RUN rm /app/CowBook/static/calendar.ics

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
VOLUME /app/CowBook/Data
VOLUME /app/CowBook/static/Pictures