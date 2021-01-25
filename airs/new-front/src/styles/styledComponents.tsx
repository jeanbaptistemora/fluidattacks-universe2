import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const NavbarContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
   cssmenu
   bg-white
   lh-solid
   h-navbar
   cover
   ba
   b--light-gray
   fixed
   w-100
   top-0
   z-max
   t-all-5
  `
})``;

const NavbarInnerContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    b
    relative
    w-100
    z-5
    mw-1366
    mr-auto
    ml-auto
    h-navbar
    ph-body
  `
})``;

const NavbarList: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
   list
   ma0
   pa0
   overflow-hidden
   h-navbar
  `
})``;

const MenuButton: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
     relative
     fl
     pv4
     mv1
    `
})``;

const NavbarContactButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
     outline-transparent
     fw7
     f-18
     br2
     bw1
     ph2
     pv2
     bg-white
     bc-fluid-red
     ba
     hv-fluid-rd
     hv-fluid-bd
     t-all-3-ease
     c-dkred
     pointer
    `
})``;

const NavbarLoginButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
     outline-transparent
     c-dkred
     fw7
     f-18
     ba
     b--white
     bw1
     ph0
     pv2
     hv-fluid-rd
     bg-transparent
     pointer
  `
})``;

const NavbarRegularButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
  outline-transparent
  fw4
  f-18
  ba
  b--white
  bw1
  ph0
  pv2
  hv-fluid-rd
  bg-transparent
  pointer
  `
})``;

const NavbarSubcategory: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    roboto
    br3
    br--bottom
    pt4
    fadein
    `
})``;

const SubcategoryLink: StyledComponent<
  "a",
  Record<string, unknown>
> = styled.a.attrs({
  className: `
    f-18
    fw4
    `
})``;

export {
  NavbarSubcategory,
  NavbarContactButton,
  NavbarContainer,
  NavbarInnerContainer,
  NavbarList,
  NavbarLoginButton,
  NavbarRegularButton,
  MenuButton,
  SubcategoryLink
};
