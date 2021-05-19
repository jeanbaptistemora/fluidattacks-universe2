{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-gitlab-etl-runtime-python";
  dependencies = [
    nixpkgs.postgresql
  ];
  requirements = {
    direct = [
      "aiohttp==3.6.2"
      "click==7.1.2"
      "nest-asyncio==1.4.1"
      "psycopg2==2.8.6"
    ];
    inherited = [
      "aioextensions==20.8.2087641"
      "asgiref==3.2.10"
      "async-timeout==3.0.1"
      "attrs==20.3.0"
      "chardet==3.0.4"
      "idna==3.1"
      "multidict==4.7.6"
      "uvloop==0.14.0"
      "yarl==1.6.3"
    ];
  };
  python = nixpkgs.python38;
}
