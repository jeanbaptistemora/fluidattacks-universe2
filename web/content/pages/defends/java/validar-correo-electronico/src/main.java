import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Main {
  public static void main(String[] args) {
    String emailPattern = "^[_a-z0-9-]+(\\.[_a-z0-9-]+)*@" +
      "[a-z0-9-]+(\\.[a-z0-9-]+)*(\\.[a-z]{2,4})$";
  Pattern pattern = Pattern.compile(emailPattern);
    String email = args[0];
  if (email != null) {
      Matcher matcher = pattern.matcher(email);
      if (matcher.matches()) {
         System.out.println("Válido");
    }
      else {
       System.out.println("NO Válido");
     }
   }
 }
}
