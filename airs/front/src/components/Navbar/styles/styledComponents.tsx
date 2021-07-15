import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const MenuDesktopInnerContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    sidenav
    bg-whitergray
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
    w-50
    dib
    fl
    ml1
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
    w-100
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
    w-100
    justify-center
    items-center
    flex
  `,
})``;

const MenuDesktopSectionList: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    list
    f5
    fw7
    ph0
    mh4
    mb4
    overlay-menu-col
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

const TopBarButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    c-fluid-gray
    hv-fluid-black
    outline-transparent
    fw4
    f-18
    ba
    b--transparent
    bw1
    ph0
    pv2
    bg-transparent
    pointer
  `,
})``;

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

const DesktopTopbarItemsContainer = styled.div.attrs({
  className: `
    w-50
    flex
    flex-nowrap
    justify-end
  `,
})``;

const DesktopTopbarItem = styled.li.attrs<{ className: string }>({
  className: `
    mr3
    pv4
  `,
})``;

export {
  BlackWeightedParagraph,
  CloseMenuButton,
  CloseMenuButtonContainer,
  DesktopTopbarItem,
  DesktopTopbarItemsContainer,
  FlexMenuItems,
  HalfWidthContainer,
  MenuDesktopContainer,
  MenuDesktopInnerContainer,
  MenuDesktopSectionList,
  MenuMobileContainer,
  MenuMobileInnerContainer,
  MenuSectionContainer,
  MenuSidebar,
  QuarterHeightContainer,
  SidebarList,
  SidebarListContainer,
  SidebarListItem,
  TopBarButton,
};
