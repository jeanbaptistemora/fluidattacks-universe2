import { PureAbility } from "@casl/ability";
import { BoundCanProps, createContextualCan } from "@casl/react";
import React from "react";
import { authzGroupContext } from "../config";

const have: React.FC<BoundCanProps<PureAbility<string>>> =
  createContextualCan(authzGroupContext.Consumer);

export { have as Have };
