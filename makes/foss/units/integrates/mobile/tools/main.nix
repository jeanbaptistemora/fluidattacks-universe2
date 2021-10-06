{ makeSearchPaths
, outputs
, ...
}:
makeSearchPaths {
  source = [
    outputs."/integrates/mobile/tools/bundler"
    outputs."/integrates/mobile/tools/fastlane"
  ];
}
