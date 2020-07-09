import { PureAbility } from "@casl/ability";
import React from "react";

export const groupAttributes: PureAbility<string> = new PureAbility<string>();
export const groupLevelPermissions: PureAbility<string> = new PureAbility<string>();
export const organizationLevelPermissions: PureAbility<string> = new PureAbility<string>();
export const userLevelPermissions: PureAbility<string> = new PureAbility<string>();

export const authzPermissionsContext: React.Context<PureAbility<string>> =
  React.createContext(new PureAbility<string>());

export const authzGroupContext: React.Context<PureAbility<string>> =
  React.createContext(new PureAbility<string>());
