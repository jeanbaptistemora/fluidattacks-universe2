// eslint-disable-next-line import/no-unresolved
import { window } from "vscode";

import { UPDATE_TOE_LINES_ATTACKED } from "../queries";
import { getClient } from "../utils/apollo";

const updateToeLinesAttackedLines = (item: {
  comments: string;
  filename: string;
  groupName: string;
  rootId: string;
}): void => {
  getClient()
    .mutate({
      mutation: UPDATE_TOE_LINES_ATTACKED,
      variables: {
        comments: item.comments,
        fileName: item.filename,
        groupName: item.groupName,
        rootId: item.rootId,
      },
    })
    .then((_result): void => {
      if (
        _result.data !== undefined &&
        // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
        (_result.data.updateToeLinesAttackedLines.success as boolean)
      ) {
        void window.showInformationMessage("line has been updated");
      }
    })
    .catch((error): void => {
      void window.showErrorMessage(String(error));
    });
};

export { updateToeLinesAttackedLines };
