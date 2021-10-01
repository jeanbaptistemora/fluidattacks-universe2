{ makes
, ...
}:
makes.makeRubyGemsEnvironment {
  name = "integrates-tools-asciidoctor";
  ruby = "2.6";
  rubyGems = [
    {
      name = "asciidoctor";
      version = "2.0.10";
      sha256 = "1b2ajs3sabl0s27r7lhwkacw0yn0zfk4jpmidg9l8lzp2qlgjgbz";
    }
  ];
}
