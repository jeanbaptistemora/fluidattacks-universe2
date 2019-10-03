class Permission {
  private Role role;
  private Resource resource;
  public Permission( Role s, Resource r) {
    role = s;
    resource = r;
  }
  public Permission( Permission p) {
    role = p.role;
    resource = p.resource;
  }
  Resource getResource() {
    return resource;
  }
  Role getRole() {
    return role;
  }
    boolean grantedTo(Role role, Resource res) {
    return(this.role.equals(role) && res.equals(resource));
  }
}
