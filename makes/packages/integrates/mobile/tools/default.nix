{ makes
, packages
, ...
}:
makes.makeSearchPaths {
  source = [
    packages.integrates.mobile.tools.bundler
    packages.integrates.mobile.tools.fastlane
  ];
}
