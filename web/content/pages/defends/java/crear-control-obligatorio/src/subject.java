class Subject
{
  private String name;
  private Sensibility clearance;
  public Subject(String n, Sensibility c)
  {
    name = n;
    clearance = c;
  }
  public String getName()
  {
    return name;
  }
  public Sensibility getClearance()
  {
    return clearance;
  }
}
