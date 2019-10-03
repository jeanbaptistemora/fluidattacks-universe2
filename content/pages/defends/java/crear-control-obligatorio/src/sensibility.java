class Sensibility
{
  int sensibility;
  // 0: unclassified
  // 1: classified
  // 2: secret
  // 3: top secret
  public Sensibility(int s)
  {
    sensibility = s;
  }
  public boolean allows(Sensibility s)
  {
    return s.sensibility >= sensibility;
  }
}
