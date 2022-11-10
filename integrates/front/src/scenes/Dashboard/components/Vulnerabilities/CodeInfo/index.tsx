/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { highlightAll } from "prismjs";
import React, { useEffect } from "react";

import type { ICodeInfoProps } from "./types";

const CodeInfo: React.FC<ICodeInfoProps> = ({
  vulnerability,
}: ICodeInfoProps): JSX.Element => {
  useEffect((): void => {
    highlightAll();
  }, []);

  return (
    <div className={"Code"}>
      <pre>
        <code className={"language-none"}>{vulnerability.snippet}</code>
      </pre>
    </div>
  );
};

export { CodeInfo };
