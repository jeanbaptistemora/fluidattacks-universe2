{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "ab71807ab735d02331a9ee4cbcfa591c1f9ef588";
  };
}
