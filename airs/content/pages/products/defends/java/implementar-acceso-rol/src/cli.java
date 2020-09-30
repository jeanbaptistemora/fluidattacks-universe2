class CLI
{
  public static void main(String[] args)
  {
    Role role1 = new Role("Rol1");
    Role role2 = new Role("Rol2");
  Subject subj0 = new Subject("Sujeto0");
  Subject subj1 = new Subject("Sujeto1");
  Subject subj2 = new Subject("Sujeto2");
  Subject subj3 = new Subject("Sujeto3");
  role1.addSubject(subj0);
  role1.addSubject(subj1);
  role2.addSubject(subj2);
  role2.addSubject(subj3);
  Resource res1 = new Resource("Recurso1");
  Permission perm1 = new Permission(role1, res1);
  AccessController.addPermission(perm1);
  AccessController.access(subj0, res1);
    AccessController.access(subj1, res1);
    AccessController.access(subj2, res1);
    AccessController.access(subj3, res1);
  }
}
