{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "7a2b256168a7a5b58cf79d9383e5b463dae9c5e5";
  };
}
