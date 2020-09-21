class AccessController
{
  private static boolean isAccessAllowed(Subject s, Resource r)
  {
    return(r.getClassification().allows(s.getClearance()));
  }
  public static void access(Subject s, Resource r)
  {
    if(isAccessAllowed(s, r))
    {
      r.access();
    }
    else
    {
      System.out.println("[AccessController] El acceso a " + r.getName() + " por " + s.getName() +
       " ha sido denegado");
    }
  }
}
