import styled from "styled-components";
import type { StyledComponent } from "styled-components";

export const NavbarContainer: StyledComponent<
"div", Record<string, unknown>
> = styled.div.attrs(
{
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
  `,
})``;

export const NavbarInnerContainer: StyledComponent<
"div", Record<string, unknown>
> = styled.div.attrs(
{
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
  `,
})``;

export const NavbarList: StyledComponent<
"ul", Record<string, unknown>
> = styled.ul.attrs(
{
  className: `
   list
   ma0
   pa0
   overflow-hidden
   h-navbar
  `,
})``;

export const MenuButton: StyledComponent<
"li", Record<string, unknown>
> = styled.li.attrs(
  {
    className: `
     relative
     fl
     pv4
     mv1
    `,
  })``;

export const NavbarContactButton: StyledComponent<
"button", Record<string, unknown>
> = styled.button.attrs(
  {
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
    `,
})``;
