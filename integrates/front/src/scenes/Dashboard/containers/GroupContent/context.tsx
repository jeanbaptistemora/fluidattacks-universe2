import { createContext } from "react";

import type { IGroupContext } from "./types";

const groupContext: React.Context<IGroupContext> = createContext({
  path: "",
  url: "",
});

export { groupContext };
