# Yan Pan
# the name is provided by AKS automatically
data "azurerm_user_assigned_identity" "ingress" {
  name                = "ingressapplicationgateway-${azurerm_kubernetes_cluster.aks.name}"
  resource_group_name = azurerm_kubernetes_cluster.aks.node_resource_group
}

# Allow AKS to pull image
resource "azurerm_role_assignment" "role_aks_acrpull" {
  scope                            = azurerm_container_registry.acr.id
  role_definition_name             = "AcrPull"
  principal_id                     = data.azurerm_user_assigned_identity.ingress.principal_id
  skip_service_principal_aad_check = true
}

# Application Gateway allow the ingress controller to gateways public IP Address
resource "azurerm_role_assignment" "role_gateway_a" {
  scope                = azurerm_resource_group.core_rg.id
  role_definition_name = "Reader"
  principal_id         = data.azurerm_user_assigned_identity.ingress.principal_id
}

resource "azurerm_role_assignment" "role_gateway_b" {
  scope                = azurerm_virtual_network.core_vnet.id
  role_definition_name = "Network Contributor"
  principal_id         = data.azurerm_user_assigned_identity.ingress.principal_id
}

resource "azurerm_role_assignment" "role_gateway_c" {
  scope                = azurerm_application_gateway.aks_gateway.id
  role_definition_name = "Contributor"
  principal_id         = data.azurerm_user_assigned_identity.ingress.principal_id
}
