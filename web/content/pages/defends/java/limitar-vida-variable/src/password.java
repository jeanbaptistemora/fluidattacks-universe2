class Password {

  public static void main (String args[]) throws IOException {
    Console c = System.console();

    if (c == null) {
      System.err.println("No console.");
      System.exit(1);
    }

    String username = c.readLine("Enter your user name: ");
    char[] password = c.readPassword("Enter your password: ");
    boolean isValidUser = verify(username, password);

    // limpiar la contraseña
    Arrays.fill(password,' ');

    if (!isValidUser) {
      throw new SecurityException("Invalid Credentials");
    }

  }

  // Validación simulada, siempre devuelve +true+
  private static final boolean verify(String username, char[] password) {
    return true;
  }
}
