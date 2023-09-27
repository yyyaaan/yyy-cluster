# YYY Cluster Orchestration

[![FastAPI-Multi-Apps](https://github.com/yyyaaan/yyy-cluster/actions/workflows/multi-apps.yaml/badge.svg)](https://github.com/yyyaaan/yyy-cluster/actions/workflows/multi-apps.yaml) [![Apps-API-and-Frontend](https://github.com/yyyaaan/yyy-cluster/actions/workflows/test-and-build.yaml/badge.svg)](https://github.com/yyyaaan/yyy-cluster/actions/workflows/test-and-build.yaml) [![vuejs-and-fluentd-docker](https://github.com/yyyaaan/yyy-cluster/actions/workflows/vuejs-and-fluentd.yaml/badge.svg)](https://github.com/yyyaaan/yyy-cluster/actions/workflows/vuejs-and-fluentd.yaml)

External modules: 

[![yBotY-app](https://github.com/yyyaaan/yBotY/actions/workflows/test-build-push-yBot.yaml/badge.svg)](https://github.com/yyyaaan/yBotY/actions/workflows/test-build-push-yBot.yaml)

---

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens) ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white) ![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D) ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)  ![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white) ![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white) ![Alpine Linux](https://img.shields.io/badge/Alpine_Linux-%230D597F.svg?style=for-the-badge&logo=alpine-linux&logoColor=white) ![Fluentd](https://img.shields.io/badge/Fluentd-599CD0?style=for-the-badge&logo=fluentd&logoColor=white&labelColor=599CD0) ![Elastic Search](https://img.shields.io/badge/Elastic_Search-005571?style=for-the-badge&logo=elasticsearch&logoColor=white
) ![Kibana](https://img.shields.io/badge/Kibana-005571?style=for-the-badge&logo=Kibana&logoColor=white)

Kubernetes Docker Compose and Terraform for my cluster orchestration, including a root nginx ingress control. Involves multiple container services from separate repos.

Link to [Docker hub yyyaaan repositories](https://hub.docker.com/repositories/yyyaaan).

## Network Security

Port 9001 is the main service entry point, routing to correct backends and the frontend; currently reversed-proxy again to 80/433 fully open to Internet.

Port 24224 is exposed to localhost as `fluentd` logging service endpoint, this port must be blocked in firewall.

`elasticsearch` and other backend services are only available within virtual network.

## Fast-API-mongo-min: centralized authentication & authorization

This light weighted `FastAPI` app has authentication model implemented, and by design:

- the public facing endpoints
- proxies to other container app
- or, mount routers from other FastAPI and add auth layer when applicable
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

## EFK Logging Service

`fluentd` container must be start before docker compose.

`elasticsearch` will be used in both logging service and as a vector storage destination.

Note that `Kibana`, as a data visualization tool is not opened in `PROD`, and it is written in `docker-compose.yaml` (dev-only). It can be configured to connect remote elasticsearch providing the allowed host and the open port.

## FastAPI Parent-Child Building

This repository contains the "parent" app that includes authentication. The `dockerfileMultiApps` will build the container image that also includes child apps, where authentication is enforced. Follow links below.

[![FastAPI-Multi-Apps](https://github.com/yyyaaan/yyy-cluster/actions/workflows/multi-apps.yaml/badge.svg)](https://github.com/yyyaaan/yyy-cluster/actions/workflows/multi-apps.yaml) 

[![Docker Hub](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/repository/docker/yyyaaan/fastapps/general)

## Nginx Ingress and MongoDB (dev-only)

While all functional units are developed in isolated environments, nginx ingress configuration and __dev-only__ MongoDB service is defined here.

__Important__ note of ingress: `nginx-ingress` shall not be used for `Kubernetes` deployment, and must be replaced by cloud-specific ingress controller. Be minded that `Kubenet` and `Docker networks` use different DNS.

```
# create new database and user for mongodb
mongosh -u $MONGO_USER -p $MONGO_PASSWORD
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

## Frontend inside FastAPI has been removed, use VueJS `frontend`

The FastAPI-APP is designed to serve only API requests. Checkpoint branch may find legacy Jinja templates.

## Cluster Deployment in `kubernetes` via `helm` 

The main use of `helm` is to set variables correctly and automatically from `terraform`

```
# helm create
helm lint
helm template . > tmp.yaml
helm install .
```