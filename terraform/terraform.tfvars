# see variables.tf for var description
name_tag = "test"
resource_tags = {
    "env"  = "test",
    "ver"  = "beta"
    "project"  = "yan-demo-prj"
}
kv_accesses = [
    {
        object_id          = "c6b8ec28-2ed5-4ac4-9410-4e9db46c1365"
        secret_permissions = ["Get", "List", "Set", "Delete", "Recover", "Backup", "Restore", "Purge"]
    },
]
location              = "West Europe"
kv_sku                = "standard"
acr_sku               = "Basic"
acr_admin_enabled     = false
aks_private_cluster   = false
aks_kubernetes_version= "1.27.3"
aks_load_balancer_sku = "standard"
aks_sys_node_count    = 2
aks_sys_node_vm_size  = "Standard_B2ms"
aks_cpu_pool_name     = "highcpu"
aks_cpu_node_count    = 2
aks_cpu_node_vm_size  = "Standard_F2s_v2"
