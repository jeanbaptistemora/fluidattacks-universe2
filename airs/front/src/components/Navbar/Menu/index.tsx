/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
/* eslint react/jsx-no-bind:0 */

import { faBars } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useState } from "react";

import { MenuDesktop } from "./MenuDesktop";
import { MenuDesktopTopBar } from "./MenuDesktopTopBar";
import { MenuMobile } from "./MenuMobile";

import {
  CenteredMaxWidthContainer,
  MenuButton,
} from "../../../styles/styledComponents";
import {
  MenuDesktopContainer,
  MenuDesktopInnerContainer,
  MenuMobileContainer,
  MenuMobileInnerContainer,
} from "../styles/styledComponents";

const Menu: React.FC = (): JSX.Element => {
  const [isOpen, setIsOpen] = useState(false);
  function toggle(): void {
    setIsOpen(!isOpen);
    if (isOpen) {
      document.body.setAttribute("style", "overflow-y: auto;");
    } else {
      document.body.setAttribute("style", "overflow-y: hidden;");
    }
  }

  return (
    <React.Fragment>
      <MenuButton onClick={toggle}>
        <div className={"lower"}>
          <span className={"pointer dib h2-l"} id={"openbtn"}>
            <FontAwesomeIcon className={"f2 c-fluid-bk"} icon={faBars} />
          </span>
        </div>
      </MenuButton>
      <MenuDesktopContainer>
        <MenuDesktopInnerContainer
          className={isOpen ? "" : "dn"}
          id={"mySidenavXl"}
        >
          <CenteredMaxWidthContainer>
            <MenuDesktopTopBar close={toggle} />
            <MenuDesktop />
          </CenteredMaxWidthContainer>
        </MenuDesktopInnerContainer>
      </MenuDesktopContainer>
      <MenuMobileContainer>
        <MenuMobileInnerContainer style={{ width: isOpen ? "100%" : "0" }}>
          <MenuMobile close={toggle} />
        </MenuMobileInnerContainer>
      </MenuMobileContainer>
    </React.Fragment>
  );
};

export { Menu };
