resource "azurerm_app_service" "not_vulnerable" {
  name                = "example-app-service"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  app_service_plan_id = azurerm_app_service_plan.example.id
  https_only          = true
  logs {
    failed_request_tracing_enabled  = true
    detailed_error_messages_enabled = true
  }
  auth_settings {
    enabled = true
  }
}


resource "azurerm_app_service" "vulnerable" {
  name                = "example-app-service"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  app_service_plan_id = azurerm_app_service_plan.example.id
  https_only          = true
  logs {
    failed_request_tracing_enabled = false
  }
  auth_settings {
    enabled = true
  }
}
