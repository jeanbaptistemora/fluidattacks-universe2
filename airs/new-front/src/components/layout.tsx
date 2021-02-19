import { CopyrightParagraph } from "../styles/styledComponents";

import React from "react";

import "tachyons/css/tachyons.min.css";
import "../styles/index.scss";

interface IChildrenProps {
  children: JSX.Element;
}

const Layout: React.FC<IChildrenProps> = ({
  children,
}: IChildrenProps): JSX.Element => (
  <React.Fragment>
    <main>{children}</main>
    <footer>
      <div className={"mb0-l mb0-m mb3 ph3 bg-white"}>
        <div className={"mw-1366 ph-body center h3"}>
          <div className={"tc nb3 fl-l"}>
            <CopyrightParagraph>
              {`Copyright © ${new Date().getFullYear()} Fluid Attacks, We hack
              your software. All rights reserved.`}
            </CopyrightParagraph>
          </div>
        </div>
      </div>
    </footer>

    <script
      async={true}
      id={"CookieDeclaration"}
      src={
        "https://consent.cookiebot.com/9c4480b4-b8ae-44d8-9c6f-6300b86e9094/cd.js"
      }
      type={"text/javascript"}
    />
  </React.Fragment>
);

export { Layout };
