# YYY Cluster Orchestration

[![FastAPI Mongo Min App](https://github.com/yyyaaan/yyy-cluster/actions/workflows/fast-api-mongo-min.yaml/badge.svg)](https://github.com/yyyaaan/yyy-cluster/actions/workflows/fast-api-mongo-min.yaml)

Kubernetes Docker Compose and Terraform for my cluster orchestration, including a root nginx ingress control. Involves multiple container services from separate repos.

Link to [Docker hub yyyaaan repositories](https://hub.docker.com/repositories/yyyaaan).

## Fast-API-mongo-min: centralized authentication & authorization

This light weighted `FastAPI` app has authentication model implemented, and by design:

- the public facing endpoints
- proxies to other container app
- other apps may only have private/internal endpoints and no need for auth

## Docker Compose, Kubernetes and Terraform

|                      | platform                                  | remarks |
|----------------------|-------------------------------------------|---------|
| `docker-compose`     | any with docker/-compose engine installed | †       |
| `kubernetes/kubectl` | managed Kubernetes (PaaS) or OpenShift    | ††      |
| `terraform`          | IaC of K8S and deps on cloud providers    | ††      |

† mainly for development and testing purpose; auto-scaling would not be possible. See [docker engine installation](https://docs.docker.com/engine/install/)

†† fine-tuning changes required for specific platform and providers. Docker image building required from each modules separately.

__Important__ note of data persistency: `docker-compose` mount local folder as volume ; this must be changed when deployed to cloud provider.

## Nginx Ingress and MongoDB (dev-only)

While all functional units are developed in isolated environments, nginx ingress configuration and __dev-only__ MongoDB service is defined here.

__Important__ note of ingress: `nginx-ingress` shall not be used for `Kubernetes` deployment, and must be replaced by cloud-specific ingress controller. Be minded that `Kubenet` and `Docker networks` use different DNS.

```
# create new database and user for mongodb
mongosh -u $MONGOU -p $MONGOP
use newdb
db.createUser({
    user: "username",
    pwd: "password",
    roles: [{ role: "readWrite", db: "newdb" }]
})
db.updateUser("username", {roles : ["readWrite"]})
db.getRole( "readWrite/userAdmin/dbOwner", { showPrivileges: true } )
```

Managed database service is always preferred.