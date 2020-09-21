import java.util.Collection;
import java.util.ArrayList;
import java.util.Iterator;

class AccessController
{
  private static Collection permissions = new ArrayList();
  private static boolean isAccessAllowed(Subject s, Resource r)
  {
    Iterator i = permissions.iterator();
    while(i.hasNext())
    {
      Permission p = (Permission) i.next();
      if(p.grantedTo(s, r))
      {
        return true;
      }
    }
    return false;
  }
  public static void addPermission(Permission p)
  {
    permissions.add(p);
  }
  public static void access(Subject s, Resource r)
  {
    if(isAccessAllowed(s, r))
    {
      r.access();
    }
    else
    {
      System.out.println ("El acceso a " + r.getName() +  " por " + s.getName() +
        " ha sido denegado");
    }
  }
}
