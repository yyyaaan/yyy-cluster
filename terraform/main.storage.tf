# Yan Pan
resource "azurerm_storage_account" "core_storage" {
    resource_group_name      = azurerm_resource_group.core_rg.name
    location                 = azurerm_resource_group.core_rg.location
    name                     = local.storage_account_name
    account_tier             = "Standard"
    account_replication_type = "LRS"
}

resource "azurerm_storage_share" "az_file_share" {
    storage_account_name = azurerm_storage_account.core_storage.name
    name                 = local.storage_share_name
    quota                = 500
}
