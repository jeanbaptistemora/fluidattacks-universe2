/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint import/no-unresolved:0 */
/* eslint react/jsx-no-bind:0 */
import { MenuDesktop } from "./MenuDesktop";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import * as closeMenuIcon from "../../../../static/images/cross.png";
import {
  CenteredMaxWidthContainer,
  MenuButton,
} from "../../../styles/styledComponents";
import {
  CloseMenuButton,
  CloseMenuButtonContainer,
  MenuDesktopInnerContainer,
} from "../styles/navbarStyledComponents";
import React, { useState } from "react";

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
            <img
              alt={"Menu open icon"}
              className={"w2"}
              src={"https://fluidattacks.com/theme/images/menu.svg"}
            />
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
                <img
                  alt={"Close Menu Icon"}
                  className={"w2"}
                  src={closeMenuIcon}
                />
              </CloseMenuButton>
            </CloseMenuButtonContainer>
            <MenuDesktop />
          </CenteredMaxWidthContainer>
        </MenuDesktopInnerContainer>
      </MenuDesktopContainer>
      <MenuMobileContainer>
        <MenuMobileInnerContainer style={{ width: isOpen ? "100%" : "0" }}>
          <CloseMenuMobileContainer>
            <CloseMenuMobile onClick={toggle} />
          </CloseMenuMobileContainer>
        </MenuMobileInnerContainer>
      </MenuMobileContainer>
    </React.Fragment>
  );
};

export { Menu };
