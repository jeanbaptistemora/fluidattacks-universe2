import scala.collection.JavaConversions._

object Password {

  def main(args: Array[String]): Unit = {
    val c = System.console()
    if (c == null) {
      System.err.println("No console.")
      System.exit(1)
    }
    val username: String = c.readLine("Enter your user name: ")
    val password: Array[Char] = c.readPassword("Enter your password: ")
    val isValidUser: Boolean = verify(username, password)
    // limpiar la contraseña
    for( a <- 0 to (password.length - 1) ) {
         password(a) = '0'
      }
    if (!isValidUser) {
      throw new SecurityException("Invalid Credentials")
    }
  }

  // Validación simulada, siempre devuelve true
  private def verify(username: String, password: Array[Char]): Boolean = true

}
