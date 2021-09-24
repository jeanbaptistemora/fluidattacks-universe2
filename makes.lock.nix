{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "619df93d26b5cef1994f82255349176ec4997a5c";
  };
}
