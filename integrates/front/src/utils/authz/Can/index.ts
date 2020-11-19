import type { BoundCanProps } from "@casl/react";
import type { PureAbility } from "@casl/ability";
import type React from "react";
import { authzPermissionsContext } from "utils/authz/config";
import { createContextualCan } from "@casl/react";

const can: React.FC<BoundCanProps<PureAbility<string>>> = createContextualCan(
  authzPermissionsContext.Consumer
);

export { can as Can };
