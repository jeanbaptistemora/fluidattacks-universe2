import { createContext } from "react";

import type { ICommentContext } from "./types";

export const commentContext: React.Context<ICommentContext> = createContext({
  replying: 0,
});
