import java.util.regex.Matcher;
import java.util.regex.Pattern;

class Main {

  public static void main(String[] args) {
      Pattern p = Pattern.compile("^[a-zA-Z'.\\s]{1,40}$");
    Matcher matcher = p.matcher(args[0]);
    boolean cadenaValida = matcher.matches();
       if (cadenaValida) {
         System.out.println("La cadena SI es válida");
       }
       else {
         System.out.println("La cadena NO es válida");
       }
   }
}
