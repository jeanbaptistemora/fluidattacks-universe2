class Reuse {

  private static bool DEBUG = true;

  static void Main(string[] args) {
    divisionPorCero();
    integerParseInt();
  }

  public static void showError(Exception e) {
    if (DEBUG){
      Console.Error.WriteLine("Error");
      Console.Error.WriteLine("Causa " + e.Source + " " + e.Message);
    }
  }

  public static void divisionPorCero() {
    try {
      int x = 4;
      int y = x;
      Console.WriteLine("Resultado: "+(22/(x-y)));
    } catch (Exception e) {
      showError(e);
    }
  }
  public static void integerParseInt() {
    try {
      Console.WriteLine("Resultado: " + int.Parse("FLUID"));
    }
    catch (Exception e) {
      showError(e);
    }
  }
}
