{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "afed4c525ba41b8cff452200faca90917df19c73";
  };
}
