using System;
using System.Text.RegularExpressions;

namespace LineaBase {

  class Program {

    static Regex re = new Regex("^[a-zA-Z'.\\s]{1,40}$");

    static void Main(string[] args) {
      string email = args[0];
      string respuesta = re.IsMatch(email, 0) ? "válido" : "NO válido";
      Console.Out.WriteLine("{0}", respuesta);
    }
  }
}
