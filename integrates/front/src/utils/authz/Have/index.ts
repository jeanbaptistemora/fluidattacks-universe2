import type { BoundCanProps } from "@casl/react";
import type { PureAbility } from "@casl/ability";
import type React from "react";
import { authzGroupContext } from "utils/authz/config";
import { createContextualCan } from "@casl/react";

const have: React.FC<BoundCanProps<PureAbility<string>>> = createContextualCan(
  authzGroupContext.Consumer
);

export { have as Have };
