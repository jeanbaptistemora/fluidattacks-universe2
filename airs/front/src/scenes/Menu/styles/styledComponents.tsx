/* eslint import/no-namespace:0 */
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
  box-shadow: 0 10px 20px 0 rgba(0, 0, 0, 0.16);
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
  fadein
  `,
})<{ isShown: boolean }>`
  display: ${({ isShown }): string => (isShown ? "flex" : "none")};
  background-color: #f4f4f6;
  align-content: center;
  justify-content: center;
  height: 90px;
`;

const ContainerWithSlide = styled.div.attrs({
  classname: `
  w-auto
  `,
})<{ isShown: boolean }>`
  display: ${({ isShown }): string => (isShown ? "block" : "none")};

  @keyframes fadeInRight {
    from {
      opacity: 0;
      transform: translateX(100%);
    }
    to {
      opacity: 1;
    }
  }
  animation: fadeInRight 0.4s ease-in-out;
`;

const SlideMenu = styled.div.attrs({
  classname: ``,
})<{ isShown: boolean; status: number }>`
  height: 300px;
  display: ${({ isShown }): string => (isShown ? "block" : "none")};
  @keyframes fadeInLeft {
    from {
      opacity: 0;
      transform: translateX(-100%);
    }
    to {
      opacity: 1;
      transform: translateX(0%);
    }
  }
  animation: ${({ status }): string =>
    status > 1 ? "fadeInLeft 0.4s ease-in-out" : ""};
`;

export {
  ContainerWithSlide,
  MenuFootContainer,
  MenuMobileContainer,
  MenuMobileInnerContainer,
  NavbarContainer,
  SlideMenu,
};
