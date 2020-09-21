import java.io.*;

public class dead {
  public static void main(String[] args) throws Exception {
      // método viejo
      // ejecutar("ls /home/fluid/");
      // método nuevo
      listarArchivos("/home/fluid");
  }

  public static void listarArchivos(String ruta) {
      File dir = new File(ruta);
    String[] archivos = dir.list();
      if (archivos != null) {
        for (int i = 0; i < archivos.length; i++) {
            System.out.println(archivos[i]);
        }
      }
      else {
        System.out.println("La ruta no existe");
      }
  }

  public static void ejecutar(String comando) throws Exception {
        String linea = "";
      String resultado = "";
       Process p = Runtime.getRuntime().exec(comando);
      BufferedReader input = new BufferedReader( new InputStreamReader(p.getInputStream()));
      while ((linea = input.readLine()) != null) {
          System.out.println(linea);
      }
      input.close();
      p.waitFor();
    }
}
