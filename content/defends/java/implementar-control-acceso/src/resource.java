class Resource
{
  private String name;
  public Resource(String n)
  {
    name = n;
  }
  public void access()
  {
    System.out.println("El recurso " + name + " fue accedido");
  }
  public String getName()
  {
    return name;
  }
  public boolean equals(Resource r)
  {
    return (r.name.equals(name));
  }
}
