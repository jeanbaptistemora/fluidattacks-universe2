{ assertsPkgs
, buildPythonRequirements
, makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcAssertsFluidasserts = path "/asserts/fluidasserts";
    envSrcAssertsSphinx = path "/asserts/sphinx";
  };
  searchPaths = {
    envPaths = [
      assertsPkgs.perl
      assertsPkgs.python37
      (buildPythonRequirements {
        name = "asserts-docs-build-pypi";
        python = assertsPkgs.python37;
        requirements = {
          direct = [
            "sphinx-autodoc-typehints==1.10.3"
            "sphinx-rtd-theme==0.4.3"
            "Sphinx==2.2.1"
          ];
          inherited = [
            "alabaster==0.7.12"
            "Babel==2.9.0"
            "botocore==1.18.4"
            "certifi==2020.12.5"
            "chardet==4.0.0"
            "colorama==0.4.3"
            "docutils==0.15.2"
            "idna==2.10"
            "imagesize==1.2.0"
            "Jinja2==2.11.3"
            "jmespath==0.10.0"
            "MarkupSafe==1.1.1"
            "packaging==20.9"
            "pyasn1==0.4.8"
            "Pygments==2.8.0"
            "pyparsing==2.4.7"
            "python-dateutil==2.8.1"
            "pytz==2021.1"
            "PyYAML==5.3.1"
            "requests==2.25.1"
            "rsa==4.5"
            "s3transfer==0.3.4"
            "six==1.15.0"
            "snowballstemmer==2.1.0"
            "sphinxcontrib-applehelp==1.0.2"
            "sphinxcontrib-devhelp==1.0.2"
            "sphinxcontrib-htmlhelp==1.0.3"
            "sphinxcontrib-jsmath==1.0.1"
            "sphinxcontrib-qthelp==1.0.3"
            "sphinxcontrib-serializinghtml==1.1.4"
            "urllib3==1.25.11"
          ];
        };
      })
    ];
    envSources = [
      packages.asserts.env
    ];
  };
  builder = path "/makes/packages/asserts/doc/build/builder.sh";
  name = "asserts-docs-build";
}
