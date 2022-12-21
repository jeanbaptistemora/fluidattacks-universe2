{lib}:
lib.buildPythonPackage rec {
  pname = "types-python-dateutil";
  version = "2.8.19.4";
  format = "setuptools";
  src = lib.fetchPypi {
    inherit pname version;
    hash = "sha256-NRqMqa/UrqZi+HwXJNLhrln59fmWkb47OxHSOTzTqqE=";
  };
  doCheck = false;
  pythonImportsCheck = [
    "dateutil-stubs"
  ];
}
