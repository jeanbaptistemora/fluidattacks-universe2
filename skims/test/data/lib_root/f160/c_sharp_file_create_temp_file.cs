using System;
using System.IO;

namespace StreamReadWrite
{
    class Program
    {
        static void Main(string[] args)
        {
            var tempPath = Path.GetTempFileName();
            var randomPath = Path.Combine(Path.GetTempPath(), Path.GetRandomFileName());

            using (var writer = new StreamWriter(tempPath))
            {
               writer.WriteLine("content");
            }
        }
    }
}
