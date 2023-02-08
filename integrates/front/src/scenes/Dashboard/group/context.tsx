import { createContext } from "react";

import type {
  IGroupContext,
  IVulnerabilitiesContext,
} from "scenes/Dashboard/group/types";

const groupContext: React.Context<IGroupContext> = createContext({
  organizationId: "",
  path: "",
  url: "",
});

const vulnerabilitiesContext: React.Context<IVulnerabilitiesContext> =
  createContext({
    openVulnerabilities: 0,
  });

export { groupContext, vulnerabilitiesContext };
