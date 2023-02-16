import type { ApolloError } from "@apollo/client";
// eslint-disable-next-line import/no-unresolved
import { window } from "vscode";

import {
  GET_GIT_ROOT,
  GET_GIT_ROOTS,
  GET_GIT_ROOTS_SIMPLE,
  GET_VULNERABILITIES,
  UPDATE_TOE_LINES_ATTACKED,
} from "../queries";
import type { IGitRoot, IVulnerability } from "../types";
import { API_CLIENT } from "../utils/apollo";

const getGroupGitRoots = async (groupName: string): Promise<IGitRoot[]> => {
  const result: { data: { group: { roots: IGitRoot[] } } } =
    await API_CLIENT.query({
      query: GET_GIT_ROOTS,
      variables: { groupName },
    });

  return result.data.group.roots.map((root): IGitRoot => {
    return { ...root, groupName };
  });
};
const getGroupGitRootsSimple = async (
  groupName: string
): Promise<IGitRoot[]> => {
  const result: { data: { group: { roots: IGitRoot[] } } } =
    await API_CLIENT.query({
      query: GET_GIT_ROOTS_SIMPLE,
      variables: { groupName },
    });

  return result.data.group.roots.map((root): IGitRoot => {
    return { ...root, groupName };
  });
};

const getGitRootVulnerabilities = async (
  groupName: string,
  rootId: string
): Promise<IVulnerability[]> => {
  const result: { data: { root: { vulnerabilities: IVulnerability[] } } } =
    await API_CLIENT.query({
      query: GET_VULNERABILITIES,
      variables: { groupName, rootId },
    }).catch(
      (err): { data: { root: { vulnerabilities: IVulnerability[] } } } => {
        void window.showErrorMessage(String(err));

        return { data: { root: { vulnerabilities: [] } } };
      }
    );

  return result.data.root.vulnerabilities;
};
const getGitRoot = async (
  groupName: string,
  rootId: string
): Promise<IGitRoot> => {
  const result: { data: { root: IGitRoot } } = await API_CLIENT.query({
    query: GET_GIT_ROOT,
    variables: { groupName, rootId },
  });

  return result.data.root;
};

const markFileAsAttacked = async (
  groupName: string,
  rootId: string,
  fileName: string,
  comments?: string
): Promise<{ success: boolean; message?: string }> => {
  const result: {
    updateToeLinesAttackedLines: { success: boolean; message?: string };
  } = (
    await API_CLIENT.mutate({
      mutation: UPDATE_TOE_LINES_ATTACKED,
      variables: {
        comments,
        fileName,
        groupName,
        rootId,
      },
    }).catch(
      (
        error: ApolloError
      ): {
        data: {
          updateToeLinesAttackedLines: { success: boolean; message?: string };
        };
      } => {
        return {
          data: {
            updateToeLinesAttackedLines: {
              message: error.message,
              success: false,
            },
          },
        };
      }
    )
  ).data;

  return result.updateToeLinesAttackedLines;
};

export {
  getGitRootVulnerabilities,
  getGroupGitRoots,
  getGitRoot,
  getGroupGitRootsSimple,
  markFileAsAttacked,
};
