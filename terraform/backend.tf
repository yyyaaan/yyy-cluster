# Yan Pan
# Backend required existence of the rg, account and container in prior!
# IN this demo, user has no rights to get storage key, therefore use local

terraform {
  # backend "azurerm" {
  #   resource_group_name  = "StatefulRG"
  #   storage_account_name = "statefulstorage001" # globally unique
  #   container_name       = "terraformstates"
  #   key                  = "terraform.tfstate"
  # }

  backend "local" {
    path = "tmptfstates/terraform.tfstate"
  }
}
