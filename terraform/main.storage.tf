# Yan Pan
resource "azurerm_storage_account" "azblob" {
    resource_group_name      = var.resource_group_name
    location                 = var.location
    name                     = var.storage_account_name
    account_tier             = "Standard"
    account_replication_type = "LRS"
}

resource "azurerm_storage_share" "azfileshare" {
    storage_account_name = azurerm_storage_account.azblob.name
    name                 = var.storage_share_name
    quota                = 500
}
