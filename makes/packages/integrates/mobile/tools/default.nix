{ makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  arguments = {
    envMobileToolsBundler = packages.integrates.mobile.tools.bundler;
    envMobileToolsFastlane = packages.integrates.mobile.tools.fastlane;
  };
  name = "integrates-mobile-tools";
  template = path "/makes/packages/integrates/mobile/tools/template.sh";
}
