# Yan Pan
resource "azurerm_container_registry" "acr" {
  resource_group_name = azurerm_resource_group.core_rg.name
  location            = azurerm_resource_group.core_rg.location
  name                = local.container_registry_name
  sku                 = var.acr_sku
  admin_enabled       = var.acr_admin_enabled
}

resource "azurerm_kubernetes_cluster" "aks" {
  resource_group_name = azurerm_resource_group.core_rg.name
  location            = azurerm_resource_group.core_rg.location
  name                = local.kubernetes_name
  dns_prefix          = local.kubernetes_name
  node_resource_group = local.kubernetes_infra_rg_name
  kubernetes_version  = var.aks_kubernetes_version
  private_cluster_enabled = var.aks_private_cluster

  default_node_pool {
    name                = "default"
    min_count           = 1
    max_count           = var.aks_sys_node_count
    vm_size             = var.aks_sys_node_vm_size
    enable_auto_scaling = true
    vnet_subnet_id      = azurerm_subnet.subnet_aks.id
  }

  # other node pools below

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"  # kubenet
    network_policy = "azure"
    load_balancer_sku = var.aks_load_balancer_sku
  }
}

resource "azurerm_kubernetes_cluster_node_pool" "aks_cpupool" {
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  name                  = var.aks_cpu_pool_name
  vm_size               = var.aks_cpu_node_vm_size
  enable_auto_scaling   = true 
  min_count             = 0
  max_count             = var.aks_cpu_node_count
  vnet_subnet_id        = azurerm_subnet.subnet_aks.id
}
