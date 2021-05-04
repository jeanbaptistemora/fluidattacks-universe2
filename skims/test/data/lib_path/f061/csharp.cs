class Test
{
    static void Main()
    {
        string s = null; // For demonstration purposes.

        try
        {
            int a = 1 / 0;
        }
        catch (SafeException e)
        {
        }
        catch (SafeException e)
        {
            // Empty
        }
    }
}
