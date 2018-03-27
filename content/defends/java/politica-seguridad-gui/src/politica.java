import java.io.*;

public class Politica {

  public static void main(String[] args) {
      readFile("D:\\fluid\\sensible.txt");
  }

  public static void readFile(String path) {
    BufferedReader reader = null;
    BufferedWriter writer = null;
    try {
      File file = new File(path);
      writer.write("harold:admin\n");
      String text;
      while ((text = reader.readLine()) != null) {
        System.out.println(text);
      }
    }
    catch (FileNotFoundException e) {
      System.err.println("File not found");
       }
    catch (IOException e) {
         System.err.println("I/O Exception");
       }
       catch (SecurityException e) {
         System.err.println("Write Denied");
       }
       finally {
         try {
           if (reader != null) {
             reader.close();
             }
              if (writer != null) {
               writer.close();
           }
         }
     catch (IOException e) {
           System.err.println("I/O Exception");
        }
     }
  }
}
