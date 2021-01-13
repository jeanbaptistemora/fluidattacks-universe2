import styled from "styled-components";
import type { StyledComponent } from "styled-components";

export const NavbarContainer: StyledComponent<
"div", Record<string, unknown>
> = styled.div.attrs(
{
  className: "cssmenu bg-white lh-solid h-navbar cover ba b--light-gray fixed w-100 top-0 z-max t-all-5",
})``;
