FROM nginx:stable-alpine

LABEL maintainer="Vitaly Panyukhin <creatiwww@yandex.ru>"

# main configuration file
RUN rm /etc/nginx/nginx.conf
COPY ./nginx.conf /etc/nginx/

# any additional configuration files
RUN rm /etc/nginx/conf.d/default.conf
COPY ./hello_app_service.conf /etc/nginx/conf.d/