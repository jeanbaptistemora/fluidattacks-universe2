import { PureAbility } from "@casl/ability";
import React from "react";
import { authzGroupContext } from "utils/authz/config";
import { BoundCanProps, createContextualCan } from "@casl/react";

const have: React.FC<BoundCanProps<PureAbility<string>>> = createContextualCan(
  authzGroupContext.Consumer
);

export { have as Have };
