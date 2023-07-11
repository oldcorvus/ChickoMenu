FROM nginx:1.18.0-alpine
LABEL MAINTAINER="mohanna rajabi moelcrow@gmail.com"
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]