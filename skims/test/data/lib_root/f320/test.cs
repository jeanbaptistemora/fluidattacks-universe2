using System;
class cipher{

   public void Encrypt()
	{
    	DirectoryEntry myDirectoryEntry = new DirectoryEntry(adPath);
		myDirectoryEntry.AuthenticationType = AuthenticationTypes.None;

		DirectoryEntry sndDirectoryEntry = new DirectoryEntry(adPath, "u", "p", AuthenticationTypes.None);
      DirectoryEntry thrdDirectoryEntry = new DirectoryEntry(adPath, "u", "p", AuthenticationTypes.Secure);
	}

}
