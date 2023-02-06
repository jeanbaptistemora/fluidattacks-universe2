// eslint-disable-next-line import/no-unresolved
import { workspace } from "vscode";

import { getClient } from "./api";

const API_CLIENT = getClient(
  (workspace.getConfiguration("retrieves").get("api_token") ?? "") ||
    (process.env.INTEGRATES_API_TOKEN ?? "")
);

export { API_CLIENT };
