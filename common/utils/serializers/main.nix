{makeTemplate, ...}:
makeTemplate {
  name = "common-python-serializers";
  searchPaths = {
    pythonPackage = [./src];
  };
}
