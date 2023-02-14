{makeTemplate, ...}:
makeTemplate {
  name = "common-python-git-self";
  searchPaths = {
    pythonPackage = [./src];
  };
}
