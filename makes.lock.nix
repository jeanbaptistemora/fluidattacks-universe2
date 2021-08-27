{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "da7d0277689ec668ac61f4b461a517239d8a2bd9";
  };
}
