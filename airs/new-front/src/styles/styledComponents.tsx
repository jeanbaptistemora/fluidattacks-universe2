import { Link } from "gatsby";
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
   fixed
   b--light-gray
   w-100
   top-0
   z-max
   t-all-5
  `,
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
  `,
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
  `,
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
    `,
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
    `,
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
  `,
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
  `,
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
    `,
})``;

const SubcategoryLink: StyledComponent<
  "a",
  Record<string, unknown>
> = styled.a.attrs({
  className: `
    f-18
    fw4
    `,
})``;

const CopyrightParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    c-fluid-bk
    b
    f6
    fw2
    roboto
    pv3
    mv0
  `,
})``;

const MainFooterInfoContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    mb0-l
    mb0-m
    mb3
    ph3
    bg-white
  `,
})``;

const InnerFooterInfoContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    mw-1366
    ph-body
    center
    h3
  `,
})``;

const CopyrightContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    tc
    nb3
    fl-l
  `,
})``;

const FooterInfoLinksContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h2
    bg-white
    b
    tc
    pv3
    fr-l
  `,
})``;

const FooterInfoLink: StyledComponent<
  "a",
  Record<string, unknown>
> = styled.a.attrs({
  className: `
    c-fluid-gray
    f6
    fw2
    mt2
    roboto
    no-underline
    hv-fluid-dkred
  `,
})``;

const GrayDash: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: `
    c-fluid-gray
    f6
  `,
})``;

const BreadcrumbContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  pv0
  mt-body
  `,
})``;

const BreadcrumbInnerContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    df
    ma-auto
    bg-fluid-black
  `,
})``;

const BreadcrumbList: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    roboto
    f6-l
    f7
    tl
    mw-1366
    ph-body
    ml-auto
    mr-auto
  `,
})``;

const Break: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs(
  {
    className: `
    ph0
  `,
  }
)``;

const BreadcrumbLink: StyledComponent<
  typeof Link,
  Record<string, unknown>
> = styled(Link)`
  box-shadow: none;
`;

const Flex: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs({
  className: `
    flex
  `,
})``;

const PageArticle: StyledComponent<
  "article",
  Record<string, unknown>
> = styled.article.attrs({
  className: `
    bg-graylight
  `,
})``;

const ArticleTitle: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    bg-white
    mw-1366
    ph-body
    ma0
    center
    c-fluid-bk
    fw7
    f1
    f-5-l
    roboto
    tc
  `,
})``;

const ArticleContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    internal
    mw-1366
    ph-body
    center
    roboto
    bg-white
    ph4-l
    ph3
    pt5-l
    pt4
    pb5
  `,
})``;

export {
  ArticleContainer,
  ArticleTitle,
  BreadcrumbContainer,
  BreadcrumbInnerContainer,
  BreadcrumbLink,
  BreadcrumbList,
  Break,
  CopyrightContainer,
  CopyrightParagraph,
  Flex,
  FooterInfoLinksContainer,
  FooterInfoLink,
  GrayDash,
  InnerFooterInfoContainer,
  NavbarSubcategory,
  NavbarContactButton,
  NavbarContainer,
  NavbarInnerContainer,
  NavbarList,
  NavbarLoginButton,
  NavbarRegularButton,
  MainFooterInfoContainer,
  MenuButton,
  PageArticle,
  SubcategoryLink,
};
