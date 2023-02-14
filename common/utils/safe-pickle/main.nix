{makeTemplate, ...}:
makeTemplate {
  name = "common-python-safe-pickle";
  searchPaths = {
    pythonPackage = [./src];
  };
}
