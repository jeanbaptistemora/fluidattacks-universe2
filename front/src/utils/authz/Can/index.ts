import { PureAbility } from "@casl/ability";
import { BoundCanProps, createContextualCan } from "@casl/react";
import React from "react";
import { authzPermissionsContext } from "../config";

const can: React.FC<BoundCanProps<PureAbility<string>>> =
  createContextualCan(authzPermissionsContext.Consumer);

export { can as Can };
