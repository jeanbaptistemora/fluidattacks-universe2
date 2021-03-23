import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const MenuDesktopInnerContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    sidenav
    bg-white
    fixed
    h-100
    w-100
    top-0
    left-0
    z-100
    overflow-y-auto
    fadein
  `,
})``;

const CloseMenuButtonContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-100
    w-10
    dib
  `,
})``;

const CloseMenuButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs(
  (
    props: React.ButtonHTMLAttributes<HTMLButtonElement>
  ): {
    className: string;
    type: "button" | "reset" | "submit";
  } => ({
    className: `
      pointer
      relative
      fl
      pv4
      mv2
      outline-transparent
      bg-transparent
      bn
    `,
    type: props.type ?? "button",
  })
)``;

const QuarterHeightContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    vh-25
    justify-center
    items-center
    flex
  `,
})``;

const FlexMenuItems: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-100
    w-60
    dib
    flex
  `,
})``;

const MenuSidebar: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-100
    w-30
    dib
    tc
  `,
})``;

const HalfWidthContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-100
    w-50
    dib
  `,
})``;

const MenuSectionContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    vh-50
    w-100
    justify-center
    items-center
    flex
    tc
  `,
})``;

const MenuDesktopSectionList: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
    list
    f5
    fw7
    tc
    ph0
  `,
})``;

const SidebarListContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    vh-50
    justify-center
    items-center
    flex
  `,
})``;

const SidebarList: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
    list
    f3
    fw7
    tc
    ph0
  `,
})``;

const SidebarListItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
    mb3
  `,
})``;

const BlackWeightedParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    f5
    fw6
    c-fluid-bk
    roboto
  `,
})``;

export {
  BlackWeightedParagraph,
  CloseMenuButton,
  CloseMenuButtonContainer,
  FlexMenuItems,
  HalfWidthContainer,
  MenuDesktopInnerContainer,
  MenuDesktopSectionList,
  MenuSectionContainer,
  MenuSidebar,
  QuarterHeightContainer,
  SidebarList,
  SidebarListContainer,
  SidebarListItem,
};
