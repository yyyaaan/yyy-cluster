# Yan Pan
# contains also input variable for eaiser use in later steps
output "acr_server" {
    value = azurerm_container_registry.acr.login_server
}
output "file_share_key" {
    value = azurerm_storage_account.core_storage.primary_access_key
    sensitive = true
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
