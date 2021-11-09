{ makeRubyGemsEnvironment
, ...
}:
makeRubyGemsEnvironment {
  name = "integrates-mobile-tools-bundler";
  ruby = "2.6";
  rubyGems = [
    {
      name = "bundler";
      version = "2.2.27";
      sha256 = "21d85c47937496b08b021df716b4eaa81e2223a04e8eba92ee9e767b9e1b3ed8";
    }
  ];
}
