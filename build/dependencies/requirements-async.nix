pkgs:

let
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
in
  {
    pyAsyncPkgIntegratesBack =
      builders.pythonPackageLocal ../../django-apps/integrates-back-async;
    pyAsyncPkgCasbinDynamodbAdapter =
      builders.pythonPackageLocal ../../django-apps/casbin-dynamodb-adapter;
    pyAsyncPkgCasbinInMemoryAdapter =
      builders.pythonPackageLocal ../../django-apps/casbin-in-memory-adapter;
    pyAsyncPkgReqs =
      builders.pythonRequirements ./requirements-async.txt;
    pyAsyncPkgReqsApp =
      builders.pythonRequirements ../../deploy/containers/deps-app/requirements.txt;
  }
