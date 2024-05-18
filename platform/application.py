import pulumi
import pulumi_kubernetes as kubernetes

def deploy_application(k8s_provider):

    nginx = kubernetes.apps.v1.Deployment("nginx",
        metadata=kubernetes.meta.v1.ObjectMetaArgs(
            name="nginx",
            namespace="default",
        ),
        spec=kubernetes.apps.v1.DeploymentSpecArgs(
            replicas=1,
            revision_history_limit=2,
            selector=kubernetes.meta.v1.LabelSelectorArgs(
                match_labels={
                    "app": "nginx",
                },
            ),
            template=kubernetes.core.v1.PodTemplateSpecArgs(
                metadata=kubernetes.meta.v1.ObjectMetaArgs(
                    annotations={
                        "prometheus.io/port": "9113",
                        "prometheus.io/scrape": "true",
                    },
                    labels={
                        "app": "nginx",
                        "env": "dev",
                        "type": "webserver",
                    },
                ),
                spec=kubernetes.core.v1.PodSpecArgs(
                    containers=[
                        kubernetes.core.v1.ContainerArgs(
                            env=[kubernetes.core.v1.EnvVarArgs(
                                name="PORT",
                                value="80",
                            )],
                            image="xkags/nginx-demo",
                            image_pull_policy="Always",
                            liveness_probe=kubernetes.core.v1.ProbeArgs(
                                http_get=kubernetes.core.v1.HTTPGetActionArgs(
                                    path="/",
                                    port=80,
                                ),
                                initial_delay_seconds=10,
                                period_seconds=15,
                            ),
                            name="nginx-webserver",
                            readiness_probe=kubernetes.core.v1.ProbeArgs(
                                http_get=kubernetes.core.v1.HTTPGetActionArgs(
                                    path="/",
                                    port=80,
                                ),
                                initial_delay_seconds=5,
                                period_seconds=10,
                            ),
                            resources=kubernetes.core.v1.ResourceRequirementsArgs(
                                limits={
                                    "memory": "64Mi",
                                },
                                requests={
                                    "cpu": "0.01",
                                    "memory": "64Mi",
                                },
                            ),
                        ),
                        kubernetes.core.v1.ContainerArgs(
                            args=["--nginx.scrape-uri=http://localhost:80/stub_status"],
                            image="nginx/nginx-prometheus-exporter:latest",
                            name="nginx-prometheus-exporter",
                            ports=[kubernetes.core.v1.ContainerPortArgs(
                                container_port=9113,
                                name="metrics",
                            )],
                        ),
                    ],
                ),
            ),
        ),
        opts=pulumi.ResourceOptions(provider=k8s_provider)
        )
    nginxdefault = kubernetes.core.v1.Service("nginxdefault",
        metadata=kubernetes.meta.v1.ObjectMetaArgs(
            name="nginx",
            namespace="default",
        ),
        spec=kubernetes.core.v1.ServiceSpecArgs(
            ports=[kubernetes.core.v1.ServicePortArgs(
                name="http",
                port=80,
                target_port=80,
            )],
            selector={
                "app": "nginx",
            },
        ),
        opts=pulumi.ResourceOptions(provider=k8s_provider)
        )
    