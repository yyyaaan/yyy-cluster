variable "resource_tags" {
    type        = map(string)
    description = "tags for all resources"
    default     = {
        env     = "undefined"
    }
}

variable "resource_group_name" {
    type        = string
    description = "RG name in Azure"
}

variable "location" {
    type        = string
    description = "Resources location in Azure"
}

variable "storage_account_name" {
    type        = string
    description = "Blob Storage Account Name"
}

variable "storage_share_name" {
    type        = string
    description = "Blob Storage Account Name"
}

variable "aks_name" {
    type        = string
    description = "AKS name in Azure"
}

variable "aks_kubernetes_version" {
    type        = string
    description = "Kubernetes version"
}

variable "aks_sys_node_count" {
    type        = number
    description = "Max number of AKS worker nodes, autoscaling is on"
    default     = 3
}

variable "aks_infra_rg_name" {
    type        = string
    description = "RG name for cluster resources in Azure"
}

variable "aks_sys_node_vm_size" {
    type        = string
    description = "Azure standard VM Size"
    default     = "Standard_B2ms"
}

variable "aks_load_balancer_sku" {
    type        = string
    description = "Kubernetes Load Balancer SKU, basic or standard"
    default     = "basic"
}

variable "acr_name" {
    type        = string
    description = "The name of container registry"
}

variable "acr_sku" {
    type        = string
    description = "The SKU name of the container registry"
    default     = "Basic"
}

variable "acr_admin_enabled" {
    type        = bool
    description = "ACR admin user enable or not"
    default     = false
}


