using System;
using System.IO;
using System.Text;

namespace mytest
{
  class MyReadFile
  {
    static void ReadFile(string fileName){

      FileStream fs = new FileStream(fileName,FileMode.Open,FileAccess.Read);

      if(fs.CanRead){

        byte[] buffer = new byte[fs.Length];
        int bytesread = fs.Read(buffer,0,buffer.Length);

        Console.WriteLine(Encoding.ASCII.GetString(buffer,0,bytesread));
      }
      fs.Flush();//limpiamos el búfer
      fs.Close();

    }

    public static void Main (string[] args)
    {
      string fileText = @"texto.txt";
      ReadFile(fileText);
    }
  }
}
