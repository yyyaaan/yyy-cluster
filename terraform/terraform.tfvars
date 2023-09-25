# see variables.tf for var description
name_tag = "alpha"
resource_tags = {
    "env"  = "test",
    "ver"  = "beta"
    "project"  = "yan-demo-prj"
}
location              = "West Europe"
acr_sku               = "Basic"
acr_admin_enabled     = false
app_gateway_tier      = "Standard_v2"
aks_private_cluster   = false
aks_kubernetes_version= "1.27.3"
aks_load_balancer_sku = "standard"
aks_sys_node_count    = 2
aks_sys_node_vm_size  = "Standard_B2ms"
aks_cpu_pool_name     = "highcpu"
aks_cpu_node_count    = 2
aks_cpu_node_vm_size  = "Standard_F2s_v2"
