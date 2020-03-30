pkgs:

let
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
in
  {
    pyPkgIntegratesBack =
      builders.pythonPackageLocal ../../django-apps/integrates-back;
    pyPkgCasbinDynamodbAdapter =
      builders.pythonPackageLocal ../../django-apps/casbin-dynamodb-adapter;
    pyPkgCasbinInMemoryAdapter =
      builders.pythonPackageLocal ../../django-apps/casbin-in-memory-adapter;
    pyPkgReqs =
      builders.pythonRequirements ./requirements.txt;
    pyPkgReqsApp =
      builders.pythonRequirements ../../deploy/containers/deps-app/requirements.txt;
  }
