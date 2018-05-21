class Subject
{
  private String name;
  public Subject(String n)
  {
    name = n;
  }
  public String getName()
  {
    return name;
  }
  public boolean equals(Subject s)
  {
    return(s.name.equals(name));
  }
}
