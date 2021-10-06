{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "8d3fc0a4e1fd59d065e7fc6469b3e5886bb90ed6";
  };
}
