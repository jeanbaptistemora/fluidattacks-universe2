pkgs:

let
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
in
  {
    pyAsyncPkgIntegratesBack =
      builders.pythonPackageLocal ../../django-apps/integrates-back-async;
    pyAsyncPkgReqs =
      builders.pythonRequirements ./requirements-async.txt;
    pyAsyncPkgReqsApp =
      builders.pythonRequirements ../../deploy/containers/deps-app/requirements.txt;
  }
