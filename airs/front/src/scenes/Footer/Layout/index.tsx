import { MatomoProvider, createInstance } from "@datapunt/matomo-tracker-react";
import hljs from "highlight.js";
import React, { useCallback, useEffect } from "react";

import { useWindowSize } from "../../../utils/hooks/useWindowSize";
import { DesktopFooter } from "../DesktopFooter";
import { MediumFooter } from "../MediumFooter";
import { MobileFooter } from "../MobileFooter";

interface IChildrenProps {
  children: JSX.Element;
}

const Layout: React.FC<IChildrenProps> = ({
  children,
}: IChildrenProps): JSX.Element => {
  const { width } = useWindowSize();
  useEffect((): void => {
    document.querySelectorAll("pre code").forEach((block): void => {
      hljs.highlightBlock(block as HTMLElement);
    });
  });

  const getFooterSize = useCallback((): JSX.Element => {
    if (width < 480) {
      return <MobileFooter />;
    } else if (width < 961) {
      return <MediumFooter />;
    }

    return <DesktopFooter />;
  }, [width]);

  const matomoInstance = createInstance({
    siteId: 1,
    urlBase: "https://fluidattacks.matomo.cloud",
  });

  return (
    <React.StrictMode>
      <MatomoProvider value={matomoInstance}>
        <div className={"bg-lightgray lh-copy ma0"}>
          <main>{children}</main>
          {getFooterSize()}
        </div>
      </MatomoProvider>
    </React.StrictMode>
  );
};

export { Layout };
