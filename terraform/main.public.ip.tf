# IP address for AKS ingress with FQDN assigned, location is that same as core
# resource "azurerm_public_ip" "aks_ingress_ip" {
#   name                = local.public_ip_name
#   resource_group_name = local.kubernetes_infra_rg_name
#   location            = azurerm_resource_group.core_rg.location
#   tags                = var.resource_tags
#   # domain_name_label   = local.public_fqdn
#   allocation_method   = "Static"
#   sku                 = "Standard"  # required

#   depends_on = [ azurerm_kubernetes_cluster.aks ]
# }
