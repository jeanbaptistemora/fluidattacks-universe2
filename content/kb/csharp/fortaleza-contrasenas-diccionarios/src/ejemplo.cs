using System.IO;

public class Dictionary {
  public static void Main(string[] args){
    try{
      string dic = "passwords.txt";
      System.Console.WriteLine(isPasswordInDictionary(dic, "123"));
      System.Console.WriteLine(isPasswordInDictionary(dic, "hello"));
      System.Console.WriteLine(isPasswordInDictionary(dic, "admin"));
      System.Console.WriteLine(isPasswordInDictionary(dic, "SystEM"));
      System.Console.WriteLine(isPasswordInDictionary(dic, "Str0n6_P4ssw0rd!"));
    }
    catch (FileNotFoundException e){
      System.Console.WriteLine("Diccionario no encontrado");
      System.Console.Error.WriteLine(e.Message);
    }
    catch (IOException e){
      System.Console.WriteLine("Error de entrada/salida de datos");
      System.Console.Error.WriteLine(e.Message);
    }
  }

  public static bool isPasswordInDictionary(string dictionaryFilePath, string password){
    StreamReader dictionary = new StreamReader(dictionaryFilePath);
    string word = "";
    while ((word = dictionary.ReadLine()) != null) {
        if (word.Length > 2 && (password.IndexOf(word, System.StringComparison.OrdinalIgnoreCase) >= 0)){
            return true;
        }
      }
      return false;
  }
}
