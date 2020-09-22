class Permission
{
  private Subject subject;
  private Resource resource;
  public Permission(Subject s, Resource r)
  {
    subject = s;
    resource = r;
  }
  public Permission (Permission p)
  {
    subject = p.subject;
    resource = p.resource;
  }
  Resource getResource()
  {
    return resource;
  }
  Subject getSubject()
  {
    return subject;
  }
  boolean grantedTo(Subject s, Resource r)
  {
    return(s.equals(subject) && r.equals(resource));
  }
}
