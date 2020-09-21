import java.security.Security;
import java.util.Iterator;
import java.util.Set;

class CLI
{
  public static void main(String[] args)
  {
    Provider[] providers = Security.getProviders();
    for (int i = 0; i < providers.length; i++)
    {
      System.out.println("\nProveedor: " + providers[i]);
      Set services = providers[i].keySet();
      for (Iterator it = services.iterator(); it.hasNext();)
      {
        String name = (String) it.next();
        System.out.println(" Servicio: " + name + " = " + providers[i].get(name));
      }
    }
  }
}
