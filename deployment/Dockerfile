FROM python:3.6-slim


# Copy in your requirements file
ADD requirements.txt /requirements.txt

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
        build-essential \
        libpcre3-dev \
        libpq-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install -r requirements.txt \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN python manage.py makemigrations \
    && python manage.py migrate

# Start service
CMD ["python", "manage.py", "runserver", "0:8000"]
# ENTRYPOINT ["/bin/bash", "-c", "python manage.py runserver 0:8000"]
