resource "azurerm_key_vault_secret" "vulnerable" {
  name         = "example_name"
  value        = "ID=userAdmin;Password=8aYHDkf73"
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "not_vulnerable" {
  name         = "secret-sauce"
  value        = "szechuan"
  key_vault_id = azurerm_key_vault.example.id
}
