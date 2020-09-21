public class Reuse {

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
    if (DEBUG) {
      System.err.println("Error!!!");
      System.err.println("Causa:::: " + e.getCause());
      System.err.println("Mensaje:::: " + e.getMessage());
    }
   }
  }

  public static void integerParseInt() {
    try {
      System.out.println("Resultado: " + Integer.parseInt("fluid"));
    }
    catch (Exception e) {
     if (DEBUG) {
        System.err.println("Error");
        System.err.println("Causa: " + e.getCause());
        System.err.println("Mensaje: " + e.getMessage());
     }
    }
  }

}
