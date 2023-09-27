resource "azurerm_key_vault" "core_kv" {
  name                       = local.key_vault_name
  location                   = azurerm_resource_group.core_rg.location
  resource_group_name        = azurerm_resource_group.core_rg.name
  sku_name                   = "premium"
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days = 7

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id
    secret_permissions = ["Set", "Get", "Delete", "List", "Purge", "Recover"]
  }
}

resource "azurerm_key_vault_access_policy" "kv_for_aks" {
  key_vault_id       = azurerm_key_vault.core_kv.id
  tenant_id          = data.azurerm_client_config.current.tenant_id
  object_id          = azurerm_kubernetes_cluster.aks.kubelet_identity.0.object_id
  secret_permissions = ["Set", "Get", "Delete", "List"]
}

resource "azurerm_key_vault_access_policy" "kv_access" {
  for_each = {
    for access_policy in var.kv_accesses :
    access_policy.object_id => access_policy
  }

  key_vault_id = azurerm_key_vault.core_kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  # looping for all ids
  object_id               = each.value.object_id
  secret_permissions      = each.value.secret_permissions
}

resource "azurerm_key_vault_secret" "core_kv_secret_1" {
  name         = "secret001"
  value        = "test-secret-abc"
  key_vault_id = azurerm_key_vault.core_kv.id
}
