FROM python:3.8.5
WORKDIR /code
COPY . .
RUN pip install --upgrade pip && pip install -r /code/requirements.txt
ADD entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD gunicorn foodgram_api.wsgi:application --bind 0.0.0.0:8000