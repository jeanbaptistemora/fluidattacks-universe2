import java.io.*;

public class Dictionary {
    public static void main(String[] args) {
        try {
            String diccionario = "C:\\passwords.txt";
            System.out.println(isPasswordInDictionary(diccionario, "123"));
            System.out.println(isPasswordInDictionary(diccionario, "hello"));
            System.out.println(isPasswordInDictionary(diccionario, "admin"));
            System.out.println(isPasswordInDictionary(diccionario, "SystEM"));
            System.out.println(isPasswordInDictionary(diccionario, "My-Str0n6_P4assw0rd!"));

        } catch (FileNotFoundException e) {
            System.err.println("Diccionario no encontrado");
        } catch (IOException e) {
            System.err.println("Error de entrada/salida de datos");
        }
    }

    public static boolean isPasswordInDictionary(String dictionaryFilePath,
                                                        String password)
                                                        throws FileNotFoundException, IOException {

        BufferedReader dictionary = new BufferedReader(new FileReader(dictionaryFilePath));

        String word = "";

        while ((word = dictionary.readLine()) != null) {
            if (password.equalsIgnoreCase(word)) {
                return true;
            }
        }

        return false;
    }
}
