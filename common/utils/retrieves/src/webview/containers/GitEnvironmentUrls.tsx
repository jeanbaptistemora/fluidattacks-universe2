/* eslint-disable react-hooks/rules-of-hooks */
import { messageHandler } from "@estruyf/vscode/dist/client";
import {
  VSCodeDataGrid,
  VSCodeDataGridCell,
  VSCodeDataGridRow,
} from "@vscode/webview-ui-toolkit/react";
import React, { useMemo, useState } from "react";
// eslint-disable-next-line import/no-extraneous-dependencies, import/no-namespace

import "../styles.css";

import type { IGitRoot } from "../../types";

const GitEnvironmentUrls = (): JSX.Element => {
  const [root, setRoot] = useState<IGitRoot>();
  const [rootId, setRootId] = useState<string>();

  useMemo((): void => {
    void messageHandler.request<string>("GET_ROOT_ID").then((msg): void => {
      setRootId(msg);
    });
  }, []);

  useMemo((): void => {
    if (rootId !== undefined) {
      void messageHandler
        .request<IGitRoot>("GET_ROOT", { rootId })
        .then((msg): void => {
          setRoot(msg);
        });
    }
  }, [rootId]);
  if (root === undefined) {
    return <div />;
  }

  return (
    <div>
      <VSCodeDataGrid>
        <VSCodeDataGridRow>
          {["url"].map((row, index): JSX.Element => {
            return (
              <VSCodeDataGridCell gridColumn={index + 1} key={row}>
                {row}
              </VSCodeDataGridCell>
            );
          })}
        </VSCodeDataGridRow>

        {root.gitEnvironmentUrls.map((item, index): JSX.Element => {
          return (
            <VSCodeDataGridRow key={item.id}>
              <VSCodeDataGridCell gridColumn={index + 1} />
              {item.url}
            </VSCodeDataGridRow>
          );
        })}
      </VSCodeDataGrid>
    </div>
  );
};

export { GitEnvironmentUrls };
