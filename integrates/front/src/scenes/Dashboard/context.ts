import { createContext } from "react";

import type { IAssignedVulnerabilitiesContext } from "scenes/Dashboard/types";

export const assignedVulnerabilitiesContext: React.Context<IAssignedVulnerabilitiesContext> =
  createContext({});
