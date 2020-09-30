public class ReuseGood {

  private static final boolean DEBUG = true;

  public static void main(String[] args) {
    divisionPorCero();
    integerParseInt();
  }

  public static void divisionPorCero() {
   try {
     System.out.println("Resultado: " + (1337 / 0));
   }
   catch (Exception e) {
     showError(e);
   }
  }

  public static void integerParseInt() {
    try {
      System.out.println("Resultado: " + Integer.parseInt("fluid"));
    }
    catch (Exception e) {
      showError(e);
    }
  }

  public static void showError(Exception e) {
    if (DEBUG) {
      System.err.println("Error");
      System.err.println("Causa: " + e.getCause());
      System.err.println("Mensaje: " + e.getMessage());
    }
  }

}
