import { PureAbility } from "@casl/ability";
import React from "react";

export const userLevelPermissions: PureAbility<string> = new PureAbility<string>();
export const groupLevelPermissions: PureAbility<string> = new PureAbility<string>();

export const authzPermissionsContext: React.Context<PureAbility<string>> =
  React.createContext(new PureAbility<string>());
