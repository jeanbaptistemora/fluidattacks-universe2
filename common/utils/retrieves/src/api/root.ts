// eslint-disable-next-line import/no-unresolved
import { window } from "vscode";

import { GET_GIT_ROOTS, GET_VULNERABILITIES } from "../queries";
import type { IGitRoot, IVulnerability } from "../types";
import { getClient } from "../utils/apollo";

const getGroupGitRoots = async (groupName: string): Promise<IGitRoot[]> => {
  const result: { data: { group: { roots: IGitRoot[] } } } =
    await getClient().query({
      query: GET_GIT_ROOTS,
      variables: { groupName },
    });

  return result.data.group.roots;
};

const getGitRootVulnerabilities = async (
  groupName: string,
  rootId: string
): Promise<IVulnerability[]> => {
  const result: { data: { root: { vulnerabilities: IVulnerability[] } } } =
    await getClient()
      .query({
        query: GET_VULNERABILITIES,
        variables: { groupName, rootId },
      })
      .catch(
        (err): { data: { root: { vulnerabilities: IVulnerability[] } } } => {
          void window.showErrorMessage(String(err));

          return { data: { root: { vulnerabilities: [] } } };
        }
      );

  return result.data.root.vulnerabilities;
};
export { getGitRootVulnerabilities, getGroupGitRoots };
