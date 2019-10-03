class CLI
{
  public static void main(String[] args)
  {
    Subject s0 = new Subject("Sujeto0");
    Subject s1 = new Subject("Sujeto1");
    Resource r1 = new Resource("Recurso1");
    Resource r2 = new Resource("Recurso2");
    Permission p = new Permission(s1, r1);
    AccessController.addPermission(p);
    AccessController.access(s0, r1);
    AccessController.access(s0, r2);
    AccessController.access(s1, r1);
    AccessController.access(s1, r2);
  }
}
