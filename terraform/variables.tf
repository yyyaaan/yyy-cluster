variable "name_tag" {
    description = "resource naming tag, usually something like dev,prod"
    default = "demo"
}

variable "resource_tags" {
    type        = map(string)
    description = "tags for all resources"
    default     = {
        env     = "undefined"
    }
}

variable "location" {
    type        = string
    description = "Resources location in Azure"
}

variable "kv_sku" {
  description = "Key vault sku name standard or premium."
  default     = "standard"
}

variable "kv_accesses" {
  type = list(object({
    object_id               = string
    secret_permissions      = list(string)
  }))
  description = "list of dict for key vault access assignment"
  default     = []
}

variable "aks_private_cluster" {
    type        = bool
    description = "Make AKS private cluster (only internal control pane)"
    default     = false
}

variable "aks_kubernetes_version" {
    type        = string
    description = "Kubernetes version"
    default     = "1.27.3"
}

variable "aks_sys_node_count" {
    type        = number
    description = "Max number of AKS worker nodes, autoscaling is on"
    default     = 3
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

variable "aks_cpu_pool_name" {
    type        = string
    description = "Kubenetes Node Pool Name for High CPU"
    default     = "highcpu"
}

variable "aks_cpu_node_count" {
    type        = number
    description = "Max number of HighCPU nodes, autoscaling is on, min is 0"
    default     = 2
}

variable "aks_cpu_node_vm_size" {
    type        = string
    description = "Azure standard VM Size, for high cpu nodes"
    default     = "Standard_F2s_v2"
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


