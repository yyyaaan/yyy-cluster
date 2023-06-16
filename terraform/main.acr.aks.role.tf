# Yan Pan
resource "azurerm_container_registry" "acr" {
  location            = var.location
  resource_group_name = var.resource_group_name
  name                = var.acr_name
  sku                 = var.acr_sku
  admin_enabled       = var.acr_admin_enabled
}

resource "azurerm_kubernetes_cluster" "aks" {
  location            = var.location
  resource_group_name = var.resource_group_name
  name                = var.aks_name
  kubernetes_version  = var.aks_kubernetes_version
  dns_prefix          = var.aks_name
  node_resource_group = var.aks_infra_rg_name

  default_node_pool {
    name                = "default"
    min_count           = 1
    max_count           = var.aks_sys_node_count
    vm_size             = var.aks_sys_node_vm_size
    enable_auto_scaling = true
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    load_balancer_sku = var.aks_load_balancer_sku
    network_plugin    = "kubenet"
  }
}

resource "azurerm_role_assignment" "aks_acrpull" {
  scope                            = azurerm_container_registry.acr.id
  role_definition_name             = "AcrPull"
  principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity.0.object_id
  skip_service_principal_aad_check = true
}
