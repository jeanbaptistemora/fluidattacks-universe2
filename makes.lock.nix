{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "07edaaf48ef0e0f199ee582bccfa8bd4750c1575";
  };
}
