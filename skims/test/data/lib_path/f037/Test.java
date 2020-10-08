public class Test {
  public static void main(String[ ] args) {
    try {
      int[] myNumbers = {1, 2, 3};
      System.out.println(myNumbers[10]);
    } catch (IndexException e) {
      if (e.toString() == "Error"){
        System.out.println("Error");
      }
      e.printStackTrace();
    }
  }
}