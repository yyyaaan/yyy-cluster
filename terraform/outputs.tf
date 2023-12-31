# Yan Pan
# contains also input variable for eaiser use in later steps
output "acr_server" {
    value = azurerm_container_registry.acr.login_server
}
output "file_share_account" {
    value = azurerm_storage_account.core_storage.name
}
output "file_share_key" {
    value = azurerm_storage_account.core_storage.primary_access_key
    sensitive = true
}
output "file_share_name" {
    value = azurerm_storage_share.az_file_share.name
}
output "rg_name" {
    value = azurerm_resource_group.core_rg.name
    sensitive = false
}
output "aks_name" {
    value = azurerm_kubernetes_cluster.aks.name
    sensitive = false
}
output "aks_rg_name" {
    value = local.kubernetes_infra_rg_name
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
