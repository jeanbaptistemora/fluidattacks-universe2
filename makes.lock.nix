{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "ce9d4ba2bf17b1e2f9ab81e82e2b96fa70340ba5";
  };
}
