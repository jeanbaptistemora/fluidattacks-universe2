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
          vulnerability.snippet === null ? 0 : vulnerability.snippet.offset
        }
      >
        <code className={"language-none"}>
          {vulnerability.snippet === null ? "" : vulnerability.snippet.content}
        </code>
      </pre>
    </div>
  );
};

export { CodeInfo };
