resource "azurerm_resource_group" "core_rg" {
    name = local.resource_group_name
    location = var.location
}
