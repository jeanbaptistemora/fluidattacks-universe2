using System;
using System.IO;

namespace FSG
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                String line;
                using (StreamReader sr = new StreamReader("Release.cs"))
                {
                    while ((line = sr.ReadLine()) != null)
                    {
                        Console.WriteLine(line);
                    }

                }
            }catch (Exception)
             {
                Console.WriteLine("File can't be opened");
             }
        }
    }
}
