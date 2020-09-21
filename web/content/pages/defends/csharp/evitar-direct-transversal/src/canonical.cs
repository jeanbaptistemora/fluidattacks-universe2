using System;
using System.IO;
using System.Text.RegularExpressions;

namespace FSG
{
  class Program
  {
    static Regex re = new Regex(@"^c:\\Windows\\Temp.*", RegexOptions.IgnoreCase);
      static void Main(string[] args)
      {
        var path = Path.GetFullPath(args[0]);

        Console.WriteLine(path);

        if (re.IsMatch(path, 0))
          {
            Console.WriteLine("Valid path");
          }
        else
          {
            Console.WriteLine("NOT valid path");
          }
            Console.ReadLine();
      }

  }
}
