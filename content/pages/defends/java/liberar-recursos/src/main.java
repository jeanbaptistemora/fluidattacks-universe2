public class Main {
  public static void main(String[] args) throws java.io.IOException {
    File archivo = null;
    FileReader lectorArchivo = null;
    BufferedReader memoriaLector = null;
    try {
      String ruta="./";
      //archivo = new File("prueba");
      archivo = new File(args[0]);
      lectorArchivo = new FileReader(archivo);
      memoriaLector = new BufferedReader(lectorArchivo);
      String linea;
      while((linea=memoriaLector.readLine())!=null){
        System.out.println(linea);
      }
    }
    catch(FileNotFoundException e){
      System.out.println("Se ha producido una excepción");
    }
    finally {
      if (lectorArchivo != null) {
        lectorArchivo.close();
      }
      if (memoriaLector != null) {
        memoriaLector.close();
      }
    }
  }
}
