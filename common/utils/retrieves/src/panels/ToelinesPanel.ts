/* eslint-disable fp/no-mutation */
import { randomUUID } from "crypto";

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
// eslint-disable-next-line import/no-extraneous-dependencies, import/no-namespace
import * as HtmlCreator from "html-creator";
import type { Disposable, Webview, WebviewPanel } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { Uri, ViewColumn, window } from "vscode";

import type { IEdge } from "../types";
import { getUri } from "../utilities/getUri";

interface IHtmlItem {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  attributes?: any;
  content: IHtmlItem[] | string;
  type: string;
}

function getHeaders(): IHtmlItem {
  const columnNames = [
    "filename",
    "attacked",
    "attacked lines",
    "loc",
    "modified",
    "comment",
  ];

  const row = columnNames.map((column: string, index: number): IHtmlItem => {
    return {
      attributes: {
        "cell-type": "columnheader",
        "grid-column": String(index + 1),
      },
      content: column,
      type: "vscode-data-grid-cell",
    };
  });

  return {
    attributes: { "row-type": "header" },
    content: row,
    type: "vscode-data-grid-row",
  };
}

function formatToeLines(toeLines: IEdge[]): IHtmlItem[] {
  return toeLines.map((item): IHtmlItem => {
    const columns = [
      item.node.filename,
      item.node.attackedLines >= item.node.loc,
      item.node.attackedLines,
      item.node.loc,
      item.node.modifiedDate,
      item.node.comments,
    ];

    return {
      content: columns.map((row, index: number): IHtmlItem => {
        return {
          attributes: { "grid-column": String(index + 1) },
          content: String(row),
          type: "vscode-data-grid-cell",
        };
      }),
      type: "vscode-data-grid-row",
    };
  });
}

export class ToeLinesPanel {
  public static currentPanel: ToeLinesPanel | undefined;

  private readonly disposables: Disposable[] = [];

  private constructor(
    private readonly currentPanel: WebviewPanel,
    extensionUri: Uri,
    toeLines: IEdge[]
  ) {
    this.currentPanel.onDidDispose(
      (): void => {
        this.dispose();
      },
      null,
      this.disposables
    );

    this.currentPanel.webview.html = this.getWebviewContent(
      this.currentPanel.webview,
      extensionUri,
      toeLines
    );
  }

  public static render(extensionUri: Uri, toeLines: IEdge[]): void {
    if (ToeLinesPanel.currentPanel) {
      ToeLinesPanel.currentPanel.currentPanel.reveal(ViewColumn.One);
    } else {
      const panel = window.createWebviewPanel(
        "showHelloWorld",
        "Toe Lines",
        ViewColumn.One,
        {
          enableScripts: true,
          localResourceRoots: [Uri.joinPath(extensionUri, "out")],
        }
      );

      ToeLinesPanel.currentPanel = new ToeLinesPanel(
        panel,
        extensionUri,
        toeLines
      );
    }
  }

  public dispose(): void {
    ToeLinesPanel.currentPanel = undefined;

    this.currentPanel.dispose();

    while (this.disposables.length) {
      const disposable = this.disposables.pop();
      if (disposable) {
        disposable.dispose();
      }
    }
  }

  // eslint-disable-next-line class-methods-use-this
  private getWebviewContent(
    webview: Webview,
    extensionUri: Uri,
    toeLines: IEdge[]
  ): string {
    const lines = formatToeLines(toeLines);
    const nonce = randomUUID();
    const webviewUri = getUri(webview, extensionUri, [
      "out",
      "webview.js",
    ]).toString();
    // eslint-disable-next-line @typescript-eslint/no-unsafe-call
    const html = new HtmlCreator([
      {
        content: [
          { attributes: { charset: "UTF-8" }, type: "meta" },
          {
            attributes: {
              content: "width=device-width, initial-scale=1.0",
              name: "viewport",
            },
            type: "meta",
          },
          {
            attributes: {
              content: `default-src 'none'; script-src 'nonce-${nonce}';`,
              "http-equiv": "Content-Security-Policy",
            },
            type: "meta",
          },
          { content: "Generated HTML", type: "title" },
        ],
        type: "head",
      },
      {
        attributes: { style: "padding: 1rem" },
        content: [
          {
            attributes: { "aria-label": "Basic" },
            content: [getHeaders(), ...lines],
            type: "vscode-data-grid",
          },
          {
            attributes: {
              nonce,
              src: webviewUri,
              type: "module",
            },
            type: "script",
          },
        ],
        type: "body",
      },
    ]);

    // eslint-disable-next-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
    return html.renderHTML();
  }
}
