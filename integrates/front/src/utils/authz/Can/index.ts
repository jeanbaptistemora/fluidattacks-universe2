import { PureAbility } from "@casl/ability";
import React from "react";
import { authzPermissionsContext } from "utils/authz/config";
import { BoundCanProps, createContextualCan } from "@casl/react";

const can: React.FC<BoundCanProps<PureAbility<string>>> = createContextualCan(
  authzPermissionsContext.Consumer
);

export { can as Can };
