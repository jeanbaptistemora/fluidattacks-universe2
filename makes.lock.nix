{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "b94764bc79b33fd29575067d76423ea10a80a9f2";
  };
}
