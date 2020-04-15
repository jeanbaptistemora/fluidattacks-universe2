import { PureAbility } from "@casl/ability";
import { BoundCanProps, createContextualCan } from "@casl/react";
import React from "react";
import { authzContext } from "../config";

const can: React.FC<BoundCanProps<PureAbility<string>>> =
  createContextualCan(authzContext.Consumer);

export { can as Can };
