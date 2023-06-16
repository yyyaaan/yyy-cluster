# Yan Pan
# contains also input variable for eaiser use in later steps
output "acr_server" {
    value = azurerm_container_registry.acr.login_server
}
output "file_share_account" {
    value = azurerm_storage_share.azfileshare.storage_account_name
}
output "file_share_name" {
    value = azurerm_storage_share.azfileshare.name
}
output "file_share_key" {
    value = azurerm_storage_account.azblob.primary_access_key
    sensitive = true
}
output "aks_name" {
    value = var.aks_name
}
output "rg_name" {
    value = var.resource_group_name
}
# if AcrPull role assignment is not possible, use the following (acr admin = true)
# output "acr_username" {
#     value = azurerm_container_registry.acr.admin_username
# }
# output "acr_password" {
#     value = azurerm_container_registry.acr.admin_password
#     sensitive = true
# }
# below are for connection with other system like kubectl
