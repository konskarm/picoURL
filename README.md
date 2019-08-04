# picoURL

## To run the source code locally:

Prerequisites: Linux OS

1. Install docker version 19.03.1: [Installation guide](https://docs.docker.com/install/)
2. Run the setup_picoURL.sh
    * Builds the docker image
    * Exposes the service in 127.0.0.1:8000
  

## To run the test suite:
After running the setup_picoURL.sh, execute the following command:
```docker run picourl_service python manage.py test```
