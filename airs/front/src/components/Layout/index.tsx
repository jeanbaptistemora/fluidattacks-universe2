import hljs from "highlight.js";
import React, { useEffect } from "react";

import { Footer } from "../Footer";

interface IChildrenProps {
  children: JSX.Element;
}

const Layout: React.FC<IChildrenProps> = ({
  children,
}: IChildrenProps): JSX.Element => {
  useEffect((): void => {
    document.querySelectorAll("pre code").forEach((block): void => {
      hljs.highlightBlock(block as HTMLElement);
    });
  });

  return (
    <React.StrictMode>
      <div className={"bg-lightgray lh-copy ma0"}>
        <main>{children}</main>

        <Footer />
      </div>
    </React.StrictMode>
  );
};

export { Layout };
