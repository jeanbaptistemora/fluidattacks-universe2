/* eslint-disable prefer-destructuring */
// eslint-disable-next-line import/no-unresolved
import { window } from "vscode";

import { getGroupGitRootsSimple, markFileAsAttacked } from "../api/root";
import { getRootInfoFromPath } from "../utils/file";

const updateToeLinesAttackedLines = async (
  item:
    | {
        comments: string;
        filename: string;
        groupName: string;
        rootId: string;
      }
    | { path: string; schema: string }
): Promise<void> => {
  // eslint-disable-next-line fp/no-let, @typescript-eslint/init-declarations
  let resultMutation;

  if ("path" in item) {
    const pathInfo = getRootInfoFromPath(item.path);
    if (pathInfo === null) {
      return;
    }

    const { fileRelativePath, groupName, nickname } = pathInfo;
    const result = await getGroupGitRootsSimple(groupName);
    const gitRoot = result.find((root): boolean => root.nickname === nickname);
    if (gitRoot === undefined) {
      return;
    }

    // eslint-disable-next-line fp/no-mutation
    resultMutation = await markFileAsAttacked(
      groupName,
      gitRoot.id,
      fileRelativePath,
      ""
    );
  } else {
    // eslint-disable-next-line fp/no-mutation
    resultMutation = await markFileAsAttacked(
      item.groupName,
      item.rootId,
      item.filename,
      item.comments
    );
  }

  if (resultMutation.success) {
    void window.showInformationMessage("The file has been updated");
  } else {
    void window.showErrorMessage(
      resultMutation.message ?? "Failed to update file"
    );
  }
};

export { updateToeLinesAttackedLines };
