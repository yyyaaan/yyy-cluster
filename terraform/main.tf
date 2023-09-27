# Yan Pan
# see the resource in main.**.terraform 

# naming convention prefixes
locals {
  resource_naming_prefix = "yan-demo-prj-${var.name_tag}"
}

# resouce naming, note that AKS needs its own rg. 
# some resource does not allow hyphen, handles here
locals {
  resource_group_name = "${local.resource_naming_prefix}-core-rg"
  storage_account_name = replace("${local.resource_naming_prefix}-storage-001", "-", "")
  storage_share_name = replace("${local.resource_naming_prefix}-file-share-001", "-", "")
  key_vault_name = replace("${local.resource_naming_prefix}-kv-001", "-", "")
  virtual_network_name = "${local.resource_naming_prefix}-vnet-001"
  subnet_kubernetes_name = "${local.resource_naming_prefix}-subnet-aks-001"
  subnet_private_name = "${local.resource_naming_prefix}-subnet-private-001"
  subnet_public_name = "${local.resource_naming_prefix}-subnet-public-001"
  network_security_pubic_name = "${local.resource_naming_prefix}-public-network-security-001"
  network_security_private_name = "${local.resource_naming_prefix}-private-network-security-001"
  container_registry_name = replace("${local.resource_naming_prefix}-file-share-001", "-", "")
  kubernetes_infra_rg_name = "${local.resource_naming_prefix}-aks-001-azure-managed-rg"
  kubernetes_name = "${local.resource_naming_prefix}-aks-001"
  public_ip_name = "${local.resource_naming_prefix}-aks-ingress-ip-001"
  public_fqdn = "${local.resource_naming_prefix}-services-001"
}

data "azurerm_client_config" "current" {}