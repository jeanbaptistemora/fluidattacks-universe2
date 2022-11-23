import { createContext } from "react";

import type { IAssignedVulnerabilitiesContext } from "scenes/Dashboard/types";

export const AssignedVulnerabilitiesContext =
  createContext<IAssignedVulnerabilitiesContext>([[], (): void => undefined]);
