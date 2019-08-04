#!/bin/bash

docker build . -t picourl_service

docker run -d -p 8000:8000 picourl_service
