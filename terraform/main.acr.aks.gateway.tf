# Yan Pan
locals {
  gateway_ip_configuration_name  = "${local.app_gateway_name}-gateway-ip-config"
  backend_address_pool_name      = "${local.app_gateway_name}-backend-address-pool"
  frontend_port_name             = "${local.app_gateway_name}-frontend-port"
  frontend_ip_configuration_name = "${local.app_gateway_name}-frontend-ip-config"
  http_setting_name              = "${local.app_gateway_name}-http-setting"
  listener_name                  = "${local.app_gateway_name}-http-listener"
  request_routing_rule_name      = "${local.app_gateway_name}-routing-rule"
}

resource "azurerm_container_registry" "acr" {
  resource_group_name = azurerm_resource_group.core_rg.name
  location            = azurerm_resource_group.core_rg.location
  name                = local.container_registry_name
  sku                 = var.acr_sku
  admin_enabled       = var.acr_admin_enabled
}

resource "azurerm_public_ip" "public_ip" {
  name                = local.app_gateway_ip_name
  resource_group_name = azurerm_resource_group.core_rg.name
  location            = azurerm_resource_group.core_rg.location
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_application_gateway" "aks_gateway" {
  name                = local.app_gateway_name
  resource_group_name = azurerm_resource_group.core_rg.name
  location            = azurerm_resource_group.core_rg.location

  sku {
    name     = var.app_gateway_tier
    tier     = var.app_gateway_tier
    capacity = 1
  }

  gateway_ip_configuration {
    name      = local.gateway_ip_configuration_name
    subnet_id = azurerm_subnet.subnet_gateway.id
  }

  frontend_port {
    name = local.frontend_port_name
    port = 80
  }

  frontend_ip_configuration {
    name                 = local.frontend_ip_configuration_name
    public_ip_address_id = azurerm_public_ip.public_ip.id
  }

  backend_address_pool {
    name = local.backend_address_pool_name
  }

  backend_http_settings {
    name                  = local.http_setting_name
    cookie_based_affinity = "Disabled"
    port                  = 80
    protocol              = "Http"
    request_timeout       = 1
  }

  http_listener {
    name                           = local.listener_name
    frontend_ip_configuration_name = local.frontend_ip_configuration_name
    frontend_port_name             = local.frontend_port_name
    protocol                       = "Http"
  }

  request_routing_rule {
    name                       = local.request_routing_rule_name
    priority                   = 100
    rule_type                  = "Basic"
    http_listener_name         = local.listener_name
    backend_address_pool_name  = local.backend_address_pool_name
    backend_http_settings_name = local.http_setting_name
  }
}

resource "azurerm_kubernetes_cluster" "aks" {
  resource_group_name     = azurerm_resource_group.core_rg.name
  location                = azurerm_resource_group.core_rg.location
  name                    = local.kubernetes_name
  dns_prefix              = local.kubernetes_name
  kubernetes_version      = var.aks_kubernetes_version
  private_cluster_enabled = var.aks_private_cluster
  node_resource_group     = local.kubernetes_infra_rg_name

  default_node_pool {
    name                = "default"
    min_count           = 1
    max_count           = var.aks_sys_node_count
    vm_size             = var.aks_sys_node_vm_size
    enable_auto_scaling = true
    vnet_subnet_id      = azurerm_subnet.subnet_aks.id
  }
  # more pools in separate resources below

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"  # kubenet
    network_policy = "azure"
    load_balancer_sku = var.aks_load_balancer_sku
  }

  ingress_application_gateway {
      gateway_id = resource.azurerm_application_gateway.aks_gateway.id
  }
}

resource "azurerm_kubernetes_cluster_node_pool" "example" {
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  name                  = var.aks_cpu_pool_name
  vm_size               = var.aks_cpu_node_vm_size
  enable_auto_scaling   = true 
  min_count             = 0
  max_count             = var.aks_cpu_node_count
  vnet_subnet_id        = azurerm_subnet.subnet_aks.id
}
