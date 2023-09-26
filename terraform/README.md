# IaC

Backend connection to Azure Storage, container must be existing. Use CLI or portal to create. The whole Resource Group is NOT to be changed by any services.

## Ingress and public IP

> Public IP for kubernetes ingress is provisioned by Terraform.

Kubernetes ingress has special annotation to use the existing one. This is to simplify the SSL challenge process. [reference doc](https://learn.microsoft.com/en-us/azure/aks/static-ip)

The Public IP resource is therefore in the same resource group as AKS. If provisioned by Kubernetes, it would be in the kubernetes' own MC_*_rg.


## Organization of IaC code

- `main.tf` contains local vars, but not any real infra
- `main.infra.name.tf` contains infra deployment code
- `backend.tf` defines the stateful storage for `tfstate`
  - if not default, `terraform init --backend-config=**bakcend.tf`
- `outputs.tf` contains variable to be shared and dependent during creation
- `providers.tf` defines Azure, most likely never changes
- `terraform.tfvars` contains environment specific variable
  - if not default,  `terraform plan --var-file=**.tfvars`

## Notes

Resource naming follows automatic naming convention (see `main.tf`)

[service endpoints & network securing group vnet subnet](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network)

Branch contains Application Gateway Ingress Controller Example.


