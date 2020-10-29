FROM python:3.8-buster

ENV PYTHONUNBUFFERED 1

RUN touch /etc/apt/sources.list.d/pgdg.list

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" >> /etc/apt/sources.list.d/pgdg.list

RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update

RUN apt-get update \
  # psycopg2 dependencies
  && apt-get install -y gcc python3-dev musl-dev \
  && apt-get install -y postgresql-server-dev-11 \
  # Pillow dependencies
  && apt-get install -y tk-dev tcl-dev \
  # CFFI dependencies
  && apt-get install -y libffi-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apt-get install -y postgresql-client

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
  && rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY . /app

WORKDIR /app
RUN mkdir -p /app/api_gateway/static

ENTRYPOINT ["/entrypoint"]
