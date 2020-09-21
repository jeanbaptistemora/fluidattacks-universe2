class Resource
{
  private String name;
  private Sensibility classification;
  public Resource(String n, Sensibility c)
  {
    name = n;
    classification = c;
  }
  public String getName()
  {
    return name;
  }
  public Sensibility getClassification()
  {
    return classification;
  }
  public void access()
  {
    System.out.println("El recurso " + name + " fue accedido");
  }
}
