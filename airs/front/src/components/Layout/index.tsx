import { MatomoProvider, createInstance } from "@datapunt/matomo-tracker-react";
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

  const matomoInstance = createInstance({
    siteId: 1,
    urlBase: "https://fluidattacks.matomo.cloud",
  });

  return (
    <React.StrictMode>
      <MatomoProvider value={matomoInstance}>
        <div className={"bg-lightgray lh-copy ma0"}>
          <main>{children}</main>

          <Footer />
        </div>
      </MatomoProvider>
    </React.StrictMode>
  );
};

export { Layout };
