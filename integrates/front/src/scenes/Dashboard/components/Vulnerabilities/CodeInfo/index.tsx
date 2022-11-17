/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { highlightAll } from "prismjs";
import React, { useEffect } from "react";

import type { ICodeInfoProps } from "./types";

import "prismjs/themes/prism-coy.css";
import "prismjs/plugins/line-highlight/prism-line-highlight.js";
import "prismjs/plugins/line-highlight/prism-line-highlight.css";

const CodeInfo: React.FC<ICodeInfoProps> = ({
  vulnerability,
}: ICodeInfoProps): JSX.Element => {
  useEffect((): void => {
    highlightAll();
  }, []);

  return (
    <div className={"Code"}>
      <pre
        className={"line-highlight"}
        data-line={String(Number(vulnerability.specific))}
        data-line-offset={
          Number(vulnerability.specific) > 10
            ? String(Number(vulnerability.specific) - 11)
            : 0
        }
      >
        <code className={"language-none"}>{vulnerability.snippet}</code>
      </pre>
    </div>
  );
};

export { CodeInfo };
