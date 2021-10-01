{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "4fd8827ff48dd82b45d343bb010cc99d407aa85b";
  };
}
