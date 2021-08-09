{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "00e8cf9bac7b5927576044de889e3adc38486fc8";
  };
}
