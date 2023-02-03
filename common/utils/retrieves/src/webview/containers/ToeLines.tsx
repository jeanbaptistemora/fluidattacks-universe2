/* eslint-disable react-hooks/rules-of-hooks */
import { messageHandler } from "@estruyf/vscode/dist/client";
import {
  VSCodeButton,
  VSCodeDataGrid,
  VSCodeDataGridCell,
  VSCodeDataGridRow,
} from "@vscode/webview-ui-toolkit/react";
import React, { useCallback, useState, useMemo } from "react";
// eslint-disable-next-line import/no-extraneous-dependencies, import/no-namespace

import "../styles.css";

import type { IGitRoot, IToeLineNode } from "../../types";
import { ToeLinesRow } from "../components/ToeLinesRow";

const ToeLines = (): JSX.Element => {
  const [toeLines, setToeLines] = useState<IToeLineNode[]>();
  const [root, setRoot] = useState<IGitRoot>();
  const [hideAttackedFiles, setHideAttackedFiles] = useState<boolean>(false);
  useMemo((): void => {
    if (!toeLines) {
      void messageHandler
        .request<IToeLineNode[]>("GET_DATA_TOE_LINES")
        .then((msg): void => {
          setToeLines(msg);
        });
    }
  }, [toeLines]);
  useMemo((): void => {
    void messageHandler.request<IGitRoot>("GET_ROOT").then((msg): void => {
      setRoot(msg);
    });
  }, []);

  return (
    <div>
      <VSCodeButton
        onClick={useCallback((): void => {
          setHideAttackedFiles(!hideAttackedFiles);
        }, [hideAttackedFiles])}
      >
        {hideAttackedFiles ? "Show attacked files" : "Hide attacked files"}
      </VSCodeButton>
      <VSCodeDataGrid>
        <VSCodeDataGridRow>
          {[
            "filename",
            "attacked",
            "attacked lines",
            "loc",
            "modified",
            "comment",
          ].map((row, index): JSX.Element => {
            return (
              <VSCodeDataGridCell gridColumn={index + 1} key={row}>
                {row}
              </VSCodeDataGridCell>
            );
          })}
        </VSCodeDataGridRow>

        {(toeLines ?? [])
          .filter((item): boolean => {
            if (hideAttackedFiles && item.attackedLines >= item.loc) {
              return false;
            }

            return Boolean(root);
          })
          .map((item): JSX.Element => {
            return (
              <ToeLinesRow
                groupName={root?.groupName ?? ""}
                key={item.filename}
                node={item}
                rootId={root?.id ?? ""}
              />
            );
          })}
      </VSCodeDataGrid>
    </div>
  );
};

export { ToeLines };
