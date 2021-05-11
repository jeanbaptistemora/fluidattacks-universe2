using System;
class CypherExample
{
    public static void Main()
    {
        int a = 0;
        int b = 2;
        int c = 3;
        if (a == 0)
        {
            b = a;
            if (b == 2){
                a = b;
                c = 43;
            }
            b = c;
            a = 3;
        }
        else
        {
            a = 1;
            b = a;
        }
        int c = 32;
        c = 34;
        Console.WriteLine(a);
        Console.WriteLine(b);
    }
}
