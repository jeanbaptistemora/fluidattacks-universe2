import { Glyphicon } from "react-bootstrap";
import { NavItem } from "styles/styledComponents";
import React from "react";

const NewsWidget: React.FC = (): JSX.Element => {
  React.useEffect((): void => {
    const script: HTMLScriptElement = document.createElement("script");

    script.setAttribute("async", "true");
    script.setAttribute("src", "https://cdn.headwayapp.co/widget.js");
    script.addEventListener("load", (): void => {
      const { Headway } = window as typeof window & {
        Headway: { init: (options: Record<string, string>) => void };
      };

      Headway.init({ account: "yZBW5y", selector: "#news", trigger: "#news" });
    });

    document.head.appendChild(script);
  }, []);

  return (
    <NavItem id={"news"}>
      <Glyphicon glyph={"bullhorn"} />
    </NavItem>
  );
};

export { NewsWidget };
