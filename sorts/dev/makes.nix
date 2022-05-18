{outputs, ...}: {
  dev = {
    sortsAssociationRules = {
      source = [
        outputs."/sorts/association-rules/env/dev"
      ];
    };
  };
}
