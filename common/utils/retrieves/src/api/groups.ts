/* eslint-disable @typescript-eslint/no-invalid-void-type */
/* eslint-disable fp/no-this */

import {
  window,
  workspace,
  // eslint-disable-next-line import/no-unresolved
} from "vscode";

import { GET_GROUPS } from "../queries";
import type { Organization } from "../types";
import { API_CLIENT } from "../utils/apollo";

const getGroups = async (): Promise<string[]> => {
  const groups: string[] = [
    ...workspace.getConfiguration("retrieves").get("extraGroups", []),
    ...(await Promise.resolve(
      API_CLIENT.query({ query: GET_GROUPS })
        .then(
          (result: {
            data: {
              me: {
                organizations: Organization[];
              };
            };
          }): string[] =>
            result.data.me.organizations
              .map((org: Organization): string[] =>
                org.groups.map((group): string => group.name)
              )
              .flat()
        )
        .catch((_err): [] => {
          void window.showErrorMessage(String(_err));

          return [];
        })
    )),
  ];

  return groups;
};

export { getGroups };
