# Nginx Webserver demo application

Nginx webserver serves a single `index.html` file that alternates between displaying `hello` and `world` strings on every refresh.

A small JavaScript function in `index.html` first checks for the `greetings` variable in local storage. If it's not set, it shows `Hello` for the first time. Then it checks for the value of `greetings` and replaces the value with `world` or `hello`.

The `ngx_http_stub_status_module` in Nginx configuration also provides basic status information at `/basic_status`.

### Nginx Configuration

The Nginx exposed port can be configured with the `PORT` environment variable. The default port number is 80, as defined in the Dockerfile.

### Local Docker Development

**Requirements**
- Container Builder (docker/podman/buildah...)

Dockerfile simply copies index.html and nginx.template into base image and run nginx in foreground mode.\
$BUILDPLATFORM default environment variable used for to support multi-platform builds. If you are working with MAC(ARM processors) and want to use it in linux kubernetes nodes. You should change platform variable with `linux/amd64`


```bash
1. docker build -t xkags/nginx-demo .
2. docker run -p 80:80 xkags/nginx-demo
```
Note: Don't forget to change exposed ports in `docker run` command if you edit default port.

### Kubernetes Deployment

The `nginx.yaml` can be used for deploying the application to a Kubernetes environment. It consists of deployment and service YAML files. The `servicetype` is not specified in the service resource. The application will get an IP inside of the Kubernetes network. For obtaining an external IP, `type: LoadBalancer` can be specified in the service definition.

The `stub_status_module` exposes metrics at the `/basic_status` URL. A side container, `nginx/nginx-prometheus-exporter`, collects these metrics and exposes them for Prometheus at port 9113.

The `PORT` environment variable can be overwritten with deployment environment definition. The Nginx template uses the environment variable. The default Dockerfile port 80 is overwritten with this variable.


Deploy nginx.yaml `kubectl apply -f nginx.yaml`\
Delete nginx.yaml `kubectl delete -f nginx.yaml`
