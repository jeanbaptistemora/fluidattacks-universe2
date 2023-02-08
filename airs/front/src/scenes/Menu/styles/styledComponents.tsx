import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const NavbarContainer = styled.div.attrs({
  className: `
  cssmenu
  lh-solid
  h-navbar
  cover
  w-100
  top-0
  z-max
  t-all-5
  `,
})`
  background-color: #ffffff;
  position: sticky;
`;

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
  sidenav
  fixed
  w-100
  left-0
  top-0
  z-max
  overflow-y-auto
  fadein
  `,
})`
  background-color: #ffffff;
  height: 100%;
  overflow: auto;
`;

const MenuFootContainer = styled.div.attrs({
  className: `
  w-100
  left-0
  bottom-0
  fixed
  `,
})<{ display: boolean }>`
  display: ${({ display }): string => (display ? "flex" : "none")};
  background-color: #f4f4f6;
  align-content: center;
  justify-content: center;
  height: 90px;
`;

export {
  MenuFootContainer,
  MenuMobileContainer,
  MenuMobileInnerContainer,
  NavbarContainer,
};
