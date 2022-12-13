import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;

public class Test {

  private static Logger logger = LogManager.getLogger(Log4jExample.class);

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

    try {
      int a = 1 / 0;
    } catch (ArithmeticException exc) {
      logger.info(exc);
    }

    try {
      int a = 1 / 0;
    } catch (ArithmeticException exc) {
      System.out.println("An error has occurred");
      logger.error(String.format("Ocurred error %s", exc.getMessage()));
    }

    try {
      int a = 1 / 0;
    } catch (ArithmeticException exc) {
      System.out.println(exc);
    }
  }
}