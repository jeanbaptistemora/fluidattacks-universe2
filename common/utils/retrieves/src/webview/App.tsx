/* eslint-disable react-hooks/rules-of-hooks */
import { messageHandler } from "@estruyf/vscode/dist/client";
import {
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
        {toeLines.map((item): JSX.Element => {
          return (
            <VSCodeDataGridRow key={item.filename}>
              {[
                item.filename,
                item.attackedLines >= item.loc,
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
