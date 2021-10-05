{ makeRubyGemsEnvironment
, ...
}:
makeRubyGemsEnvironment {
  name = "integrates-tools-concurrent-ruby";
  ruby = "2.6";
  rubyGems = [
    {
      name = "concurrent-ruby";
      sha256 = "094387x4yasb797mv07cs3g6f08y56virc2rjcpb1k79rzaj3nhl";
      version = "1.1.6";
    }
  ];
}
