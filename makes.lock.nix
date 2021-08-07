{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "8f5183a2e42666262c6e1d25d21acd7341e79a7d";
  };
}
