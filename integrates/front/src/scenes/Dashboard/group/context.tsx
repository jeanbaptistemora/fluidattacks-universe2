import { createContext } from "react";

import type { IGroupContext } from "./types";

const groupContext: React.Context<IGroupContext> = createContext({
  organizationId: "",
  path: "",
  url: "",
});

export { groupContext };
