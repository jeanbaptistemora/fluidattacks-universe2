/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
/* eslint react/jsx-no-bind:0 */
import { faBars, faTimes } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useState } from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { MenuDesktop } from "./MenuDesktop";
import { MenuMobile } from "./MenuMobile";

import {
  CenteredMaxWidthContainer,
  MenuButton,
} from "../../../styles/styledComponents";
import {
  CloseMenuButton,
  CloseMenuButtonContainer,
  MenuDesktopInnerContainer,
} from "../styles/navbarStyledComponents";

const MenuDesktopContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    db-l
    dn
  `,
})``;

const MenuMobileContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    dn-l
  `,
})``;

const MenuMobileInnerContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    t-all-5
    fixed
    h-100
    top-0
    left-0
    z-100
    flex
  `,
})``;

const CloseMenuMobileContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-80-m
    w-50
    h-100
  `,
})``;

const CloseMenuMobile: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    h-100
    bg-gray-black
    o-50
  `,
})``;

const Menu: React.FC = (): JSX.Element => {
  const [isOpen, setIsOpen] = useState(false);
  function toggle(): void {
    setIsOpen(!isOpen);
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
          <CenteredMaxWidthContainer className={"flex"}>
            <CloseMenuButtonContainer>
              <CloseMenuButton onClick={toggle}>
                <FontAwesomeIcon
                  className={"f1 nt2 nl2 c-fluid-gray"}
                  icon={faTimes}
                />
              </CloseMenuButton>
            </CloseMenuButtonContainer>
            <MenuDesktop />
          </CenteredMaxWidthContainer>
        </MenuDesktopInnerContainer>
      </MenuDesktopContainer>
      <MenuMobileContainer>
        <MenuMobileInnerContainer style={{ width: isOpen ? "100%" : "0" }}>
          <MenuMobile />
          <CloseMenuMobileContainer>
            <CloseMenuMobile onClick={toggle} />
          </CloseMenuMobileContainer>
        </MenuMobileInnerContainer>
      </MenuMobileContainer>
    </React.Fragment>
  );
};

export { Menu };
