FROM --platform=$BUILDPLATFORM nginx:1.25.5-alpine

ENV PORT 80

COPY nginx/index.html /etc/nginx/html/index.html
COPY nginx/nginx.template /etc/nginx/templates/default.conf.template

CMD ["nginx", "-g", "daemon off;"]