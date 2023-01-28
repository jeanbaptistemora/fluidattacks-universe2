resource "azurerm_linux_virtual_machine" "vulnerable" {
  name           = "example-machine"
  size           = "Standard_F2"
  admin_username = "adminuser"

}

resource "azurerm_linux_virtual_machine" "not_vulnerable" {
  name           = "example-machine"
  size           = "Standard_F2"
  admin_username = "adminuser"

  admin_ssh_key {
    username   = "adminuser"
    public_key = file("~/.ssh/id_rsa.pub")
  }
}
