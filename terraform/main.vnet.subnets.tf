# Yan Pan
# 256 for public and private subnets, 65536 for AKS
# see netowrk security for 

resource "azurerm_virtual_network" "core_vnet" {
  resource_group_name = azurerm_resource_group.core_rg.name
  location            = azurerm_resource_group.core_rg.location
  name                = local.virtual_network_name
  address_space       = ["10.0.0.0/8", "192.168.0.0/16"]
  tags                = var.resource_tags

  # subnet defined below (to have a simple name)
  # ddos protection plan is set outside terraform. default will disable
  lifecycle {
    ignore_changes = [ddos_protection_plan]
  }
}

resource "azurerm_subnet" "subnet_aks" {
  resource_group_name  = azurerm_resource_group.core_rg.name
  virtual_network_name = azurerm_virtual_network.core_vnet.name
  name                 = local.subnet_kubernetes_name
  address_prefixes     = ["10.1.0.0/16"]   
}

resource "azurerm_subnet" "subnet_private" {
  resource_group_name  = azurerm_resource_group.core_rg.name
  virtual_network_name = azurerm_virtual_network.core_vnet.name
  name                 = local.subnet_private_name
  address_prefixes     = ["192.168.100.0/24"]
}

resource "azurerm_subnet" "subnet_gateway" {
  resource_group_name  = azurerm_resource_group.core_rg.name
  virtual_network_name = azurerm_virtual_network.core_vnet.name
  name                 = local.subnet_gateway_name
  address_prefixes     = ["192.168.2.0/24"]   
}

resource "azurerm_subnet" "subnet_public" {
  resource_group_name  = azurerm_resource_group.core_rg.name
  virtual_network_name = azurerm_virtual_network.core_vnet.name
  name                 = local.subnet_public_name
  address_prefixes     = ["192.168.1.0/24"]
}
