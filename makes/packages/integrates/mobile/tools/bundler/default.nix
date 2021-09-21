{ makes
, ...
}:
makes.makeRubyGemsEnvironment {
  name = "integrates-mobile-tools-bundler";
  ruby = "2.6";
  rubyGems = [
    {
      name = "bundler";
      version = "2.2.6";
      sha256 = "14s8gq82h6q2kqkj5rvkc4dymaisqg1004zw7b72kc19a1kgn3ql";
    }
  ];
}
