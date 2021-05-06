using System;
class CypherExample
{
    public static void Main()
    {
        int a = 0;
        int b = 2;
        if (a == 0)
        {
            b = a;
        }
        else
        {
            a = 1;
            b = a;
        }

        Console.WriteLine(a);
        Console.WriteLine(b);
    }
}
