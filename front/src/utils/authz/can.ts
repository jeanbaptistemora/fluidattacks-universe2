import { PureAbility } from "@casl/ability";
import { BoundCanProps, createContextualCan } from "@casl/react";
import React from "react";

export const authzContext: React.Context<PureAbility<string>> =
  React.createContext(new PureAbility());

const can: React.FC<BoundCanProps<PureAbility<string>>> =
  createContextualCan(authzContext.Consumer);

export { can as Can };
