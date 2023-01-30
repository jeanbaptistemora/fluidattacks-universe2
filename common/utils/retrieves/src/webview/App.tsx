/* eslint-disable react-hooks/rules-of-hooks */
import { messageHandler } from "@estruyf/vscode/dist/client";
import {
  VSCodeButton,
  VSCodeDataGrid,
  VSCodeDataGridCell,
  VSCodeDataGridRow,
  VSCodeLink,
} from "@vscode/webview-ui-toolkit/react";
import { useCallback, useState } from "react";
// eslint-disable-next-line import/no-extraneous-dependencies, import/no-namespace
import * as React from "react";

import "./styles.css";

import type { IToeLineNode } from "../types";

const App = (): JSX.Element => {
  const [toeLines, setToeLines] = useState<IToeLineNode[]>([]);
  const [hideAttackedFiles, setHideAttackedFiles] = useState<boolean>(false);

  const useOpenFile = useCallback(
    // eslint-disable-next-line @typescript-eslint/explicit-function-return-type
    (name: string) => (): void => {
      messageHandler.send("TOE_LINES_OPEN_FILE", { message: name });
    },
    []
  );
  void messageHandler
    .request<IToeLineNode[]>("GET_DATA_TOE_LINES")
    .then((msg): void => {
      setToeLines(msg);
    });

  return (
    <div className={"app"}>
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

        {toeLines
          .filter((item): boolean => {
            if (hideAttackedFiles && item.attackedLines >= item.loc) {
              return false;
            }

            return true;
          })
          .map((item): JSX.Element => {
            return (
              <VSCodeDataGridRow key={item.filename}>
                {[
                  item.filename,
                  String(item.attackedLines >= item.loc),
                  item.attackedLines,
                  item.loc,
                  item.modifiedDate,
                  item.comments,
                ].map((cell, index): JSX.Element => {
                  return (
                    <VSCodeDataGridCell gridColumn={index + 1} key={undefined}>
                      {index === 0 ? (
                        <VSCodeLink
                          href={cell}
                          // eslint-disable-next-line line-comment-position, no-inline-comments
                          onClick={useOpenFile(String(cell))} // NOSONAR
                        >
                          {cell}
                        </VSCodeLink>
                      ) : (
                        cell
                      )}
                    </VSCodeDataGridCell>
                  );
                })}
              </VSCodeDataGridRow>
            );
          })}
      </VSCodeDataGrid>
    </div>
  );
};

export { App };
