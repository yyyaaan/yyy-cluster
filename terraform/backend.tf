# Yan Pan
terraform {
  backend "azurerm" {
    resource_group_name  = "StatefulRG"
    storage_account_name = "statefultrialdemoprj001" 
    container_name       = "terraform"
    key                  = "terraform.tfstate"
  }

  # Backend required existence of the rg, account and container in prior!
  # backend "local" {
  #   path = "tmptfstates/terraform.tfstate"
  # }
}
