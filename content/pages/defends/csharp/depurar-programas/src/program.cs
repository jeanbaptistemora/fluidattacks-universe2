using System;
class Program
{
    static void Main(string[] args)
    {
#if DEBUG
        Console.WriteLine("Using preprocessor");
#endif
    }
}
