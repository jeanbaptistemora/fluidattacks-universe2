resource "azurerm_app_service" "vulnerable" {
  name                = var.functionapp_name
  location            = var.rg_location
  resource_group_name = var.resource_group_name
  app_service_plan_id = var.asp_id
  tags                = var.modtags
}

resource "azurerm_app_service" "not_vulnerable" {
  name                = var.functionapp_name
  location            = var.rg_location
  resource_group_name = var.resource_group_name
  app_service_plan_id = var.asp_id
  https_only          = true
  tags                = var.modtags
}

resource "azurerm_function_app" "vulnerable" {
  name                       = "test-azure-functions"
  location                   = azurerm_resource_group.example.location
  resource_group_name        = azurerm_resource_group.example.name
  app_service_plan_id        = azurerm_app_service_plan.example.id
  storage_account_name       = azurerm_storage_account.example.name
  https_only                 = false
  storage_account_access_key = azurerm_storage_account.example.primary_access_key
  os_type                    = "linux"
  version                    = "~3"
}

resource "azurerm_function_app" "not_vulnerable" {
  name                       = "test-azure-functions"
  location                   = azurerm_resource_group.example.location
  resource_group_name        = azurerm_resource_group.example.name
  app_service_plan_id        = azurerm_app_service_plan.example.id
  storage_account_name       = azurerm_storage_account.example.name
  storage_account_access_key = azurerm_storage_account.example.primary_access_key
  https_only                 = true
  os_type                    = "linux"
  version                    = "~3"
}
