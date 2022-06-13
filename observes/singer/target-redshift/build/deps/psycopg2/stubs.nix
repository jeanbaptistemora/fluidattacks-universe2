lib:
lib.buildPythonPackage rec {
  pname = "types-psycopg2";
  version = "2.9.9";
  src = lib.fetchPypi {
    inherit pname version;
    sha256 = "T51NUu6zQ9wA/V7U8VE6ilwY77oKBy64JwbRXPTyCi4=";
  };
}
