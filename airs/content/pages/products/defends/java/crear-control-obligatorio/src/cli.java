class CLI
{
  public static void main(String[] args)
  {
    Sensibility normal = new Sensibility(0);
    Sensibility confidential = new Sensibility(1);
    Sensibility secret = new Sensibility(2);
    Subject s0 = new Subject("Sujeto0", normal);
    Subject s1 = new Subject("Sujeto1", confidential);
    Resource r1 = new Resource("Recurso1", confidential);
    Resource r2 = new Resource("Recurso2", secret);
    AccessController.access(s0, r1);
    AccessController.access(s0, r2);
    AccessController.access(s1, r1);
    AccessController.access(s1, r2);
  }
}
