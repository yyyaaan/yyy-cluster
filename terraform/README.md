# IaC

Backend connection to Azure Storage, container must be existing. Use CLI or portal to create. The whole Resource Group is NOT to be changed by any services.

## Resources Model

VNET, AKS, AGIC (application gateway ingress controller) are provisioned in Terraform.

Ingress router, services and all application functionality in Kubernetes.

## Organization of IaC code

- `main.tf` contains local vars, but not any real infra
- `main.infra.name.tf` contains infra deployment code
- `backend.tf` defines the stateful storage for `tfstate`
- `outputs.tf` contains variable to be shared and dependent during creation
- `providers.tf` defines Azure, most likely never changes
- `terraform.tfvars` contains environment specific variable
  - if not default,  `terraform plan --var-file=**.tfvars`

## Notes

Resource naming follows automatic naming convention (see `main.tf`)

[service endpoints & network securing group vnet subnet](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network)


```
terraform init
terraform plan -out=tfplannew
terraform apply tfplannew
```