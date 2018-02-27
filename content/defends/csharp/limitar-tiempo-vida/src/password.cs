using System;
using System.Security;

class Password
{
	static void Main(string[] args)
	{
		Console.WriteLine("Enter your user name: ");
		var loginid = Console.ReadLine();
		Console.WriteLine("Enter your password: ");
		var password = Console.ReadLine();
		char[] mArray = password.ToCharArray();

		bool isValidUser = verify(loginid, mArray);

		// limpiar la contraseña
		MyArray.Fill(mArray,' ');

		if (!isValidUser)
		{
			throw new SecurityException("Invalid Credentials");
		}
	}

	// Validación simulada, siempre devuelve true
	private static bool verify(string username, char[] password)
	{
		return true;
	}
}

internal static class MyArray
{

	internal static void Fill<T>(T[] array, T value)
	{
		for (int i = 0; i < array.Length; i++)
		{
			array[i] = value;
		}
	}

}