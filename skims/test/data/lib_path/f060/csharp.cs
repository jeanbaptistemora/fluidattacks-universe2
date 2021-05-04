class TryFinallyTest
{
    static void ProcessString(string s)
    {
        if (s == null)
        {
            throw new System.IndexOutOfRangeException();
        }
    }

    static void Main()
    {
        string s = null; // For demonstration purposes.

        try
        {
            ProcessString(s);
        }
        catch (Exception e)
        {
            Console.WriteLine("{0} Exception caught.", e);
        }
        catch (NullReferenceException e)
        {
            Console.WriteLine("{0} Exception caught.", e);
        }
        catch (System.ApplicationException e)
        {
            Console.WriteLine("{0} Exception caught.", e);
        }
        catch (SafeException e)
        {
            Console.WriteLine("{0} Exception caught.", e);
        }
    }
}
