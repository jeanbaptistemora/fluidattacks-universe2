{ makesPkgs
, path
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path makesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path makesPkgs;
in
makeEntrypoint {
  arguments = {
    envSearchPaths = makeSearchPaths [
      makesPkgs.nodejs
      makesPkgs.git
    ];
    envUtilsCommon = path "/makes/utils/common/template.sh";
    envSetupCommitlint = import (path "/makes/packages/makes/commitlint") attrs.copy;
  };
  name = "makes-lint-commit-msg";
  template = path "/makes/applications/makes/lint-commit-msg/entrypoint.sh";
}
