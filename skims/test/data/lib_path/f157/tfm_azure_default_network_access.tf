resource "azurerm_storage_account_network_rules" "not_vulnerable" {
  resource_group_name  = azurerm_resource_group.test.name
  storage_account_name = azurerm_storage_account.test.name

  default_action = "Deny"
}


resource "azurerm_storage_account" "not_vulnerable" {
  name                = var.watcher
  resource_group_name = azurerm_resource_group.test.name
  location            = azurerm_resource_group.test.location

  network_rules {
    default_action = "Deny"
  }

  account_tier              = "Standard"
  account_kind              = "StorageV2"
  account_replication_type  = "LRS"
  enable_https_traffic_only = true
  min_tls_version           = "TLS1_2"

  queue_properties {
    logging {
      delete = true
      read   = true
      write  = true
    }
  }
}

resource "azurerm_storage_account_network_rules" "vulnerable" {
  resource_group_name  = azurerm_resource_group.test.name
  storage_account_name = azurerm_storage_account.test.name

  default_action = "Allow"
}


resource "azurerm_storage_account" "vulnerable" {
  name                = var.watcher
  resource_group_name = azurerm_resource_group.test.name
  location            = azurerm_resource_group.test.location

  network_rules {
    default_action = "Allow"
  }

  account_tier              = "Standard"
  account_kind              = "StorageV2"
  account_replication_type  = "LRS"
  enable_https_traffic_only = true
  min_tls_version           = "TLS1_2"

  queue_properties {
    logging {
      delete = true
      read   = true
      write  = true
    }
  }
}
