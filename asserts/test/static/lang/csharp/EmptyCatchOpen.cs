using System;

public class Example
{
    public static void Main()
    {
        try
        {
            int[] a = new int[7];
            a[4]=30/0;
            //Console.WriteLine("First print statement in try block");
        }

        catch(ArithmeticException e)
        {

        }

        catch(IndexOutOfRangeException e)
        {
            // Oneline comment
        }

        catch(Exception e)
        {
            /*
            Multiline comment
            Test
            */
        }

        catch (Exception)
        {
        }

        try {var a = 1 / 0;} catch () { /* Seen in real life */ }

    }
/*
    try
    {
        Console.WriteLine("Out of try-catch block...");
        catch(Exception e)
        {
            Debug.WriteLine("Warning: Some Other exception");
        }
*/
}
