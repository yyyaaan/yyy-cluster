# YYY Cluster Orchestration

Kubernetes Docker Compose and Terraform for my cluster orchestration, including a root nginx ingress control. Involves multiple container services from separate repos.

Link to [Docker hub yyyaaan repositories](https://hub.docker.com/repositories/yyyaaan).

## Docker Compose, Kubernetes and Terraform

|                      | platform                                  | remarks |
|----------------------|-------------------------------------------|---------|
| `docker-compose`     | any with docker/-compose engine installed | †       |
| `kubernetes/kubectl` | managed Kubernetes (PaaS) or OpenShift    | ††      |
| `terraform`          | IaC of K8S and deps on cloud providers    | ††      |

† mainly for development and testing purpose; auto-scaling would not be possible. See [docker engine installation](https://docs.docker.com/engine/install/)

†† fine-tuning changes required for specific platform and providers. Docker image building required from each modules separately.

__Important__ note of data persistency: `docker-compose` mount local folder as volume ; this must be changed when deployed to cloud provider.

## Nginx Ingress, Dev-MongoDB, Dev-Redis

While all functional units are developed in isolated environments, nginx ingress configuration and __dev-only__ MongoDB service is defined here.

__Important__ note of ingress: `nginx-ingress` shall not be used for `Kubernetes` deployment, and must be replaced by cloud-specific ingress controller. Be minded that `Kubenet` and `Docker networks` use different DNS.

```
# create new database and user for mongodb
mongosh -u $MONGOU -p $MONGOP
use newdbname
db.createUser({
    user: "admin",
    pwd: "password",
    roles: [{ role: "userAdmin", db: "newdbname" }]
})
```

Managed database service is always preferred.