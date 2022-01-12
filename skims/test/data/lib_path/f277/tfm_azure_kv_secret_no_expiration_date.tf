resource "azurerm_key_vault_secret" "vulnerable" {
  name         = "example"
  value        = var.value_azsqlrevapp
  key_vault_id = data.azurerm_key_vault.kv.id
}

resource "azurerm_key_vault_secret" "not_vulnerable" {
  name            = "kvAzsqlRevApphist"
  expiration_date = "2020-12-30T20:00:00Z"
  value           = var.value_azsqlrevapphist
  key_vault_id    = data.azurerm_key_vault.kv.id
}
