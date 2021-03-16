/* eslint import/no-namespace:0 */
import { Link } from "gatsby";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import * as coverMainHome from "../../static/images/home/cover-main.png";

const NavbarContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
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
     hv-bd-fluid-red
     t-all-3-eio
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
  b--transparent
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
    bg-lightgray
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

const FontAwesomeContainerSmall: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    dib
    fr
    mh1
  `,
})`
  width: 0.7rem;
`;

const MainCoverHome: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  flex-ns
  items-center
  cover-m
  cover-s
  bg-banner-sz
  h-section
  `,
})`
  background-image: url(${coverMainHome});
`;

const MainContentHome: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    mt-body
    ph-body
    mw-1366
    center
    w-100
  `,
})``;

const InnerMainContentHome: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    fr-l
    w-50-l
    w100-m
    mt3-l
    center
    pt0-ns
    pt4
    pl3
  `,
})``;

const BlackBigHeader: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    f1
    c-fluid-bk
    fw6
    tl
    tc-m
    neue
    lh-solid
    ma0
  `,
})``;

const BlackBigParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    f1
    c-fluid-bk
    fw6
    tl
    tc-m
    neue
    lh-solid
    ma0
  `,
})``;

const GrayBigParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    f1
    c-fluid-gray
    fw6
    tl
    tc-m
    neue
    lh-solid
    ma0
  `,
})``;

const BlackSimpleParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    roboto
    f5
    c-fluid-bk
    lh-copy
    fw3
    ma0
  `,
})``;

const PlayItButtonContainer: StyledComponent<
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
      roboto
      f4
      c-black-gray
      justify-center
      items-center
      flex
      t-tf-6-eio
      outline-transparent
      bg-transparent
      bn
      pointer
      hv-grow
      w5
      center
    `,
    type: props.type ?? "button",
  })
)``;

const PlayItButtonImage: StyledComponent<
  "img",
  Record<string, unknown>
> = styled.img.attrs({
  className: `
    hv-rotate-360
    t-tf-6-eio
    w4
    ba
    br-100
    mh2
    bc-black-gray
  `,
})``;

const GetDemoContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-80-l
    ba
    b--light-gray
    pa4
    mt4
  `,
})``;

const BannerContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    bg-banner-sz
    nt-5
    cover
    h-banner
    justify-center
    items-center
    flex bg-center
  `,
})``;

const FullWidthContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    center
  `,
})``;

const BannerTitle: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    white
    fw7
    f1
    neue
    tc
    f-5-l
    ma0
  `,
})``;

const PageContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    roboto
    mw-1366
    ph-body
    center
    c-lightblack
    pv5
  `,
})``;

const HalfScreenContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
   w-50-l
   ph0-ns
   ph-body
  `,
})``;

const HalfScreenContainerSpaced: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-50-l
    ph-body
  `,
})``;

const SolutionsSectionDescription: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
    tl
    roboto
    list
    pl0
    mw-20
  `,
})``;

const BlackListItemSpaced: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
    c-fluid-bk
    pv3
  `,
})``;

const SolutionsSubtitle: StyledComponent<
  "h3",
  Record<string, unknown>
> = styled.h3.attrs({
  className: `
    f3
    fw6
    mv0
    underline-title
  `,
})``;

const SolutionsParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    f-1125
    lh-2
    fw3
    mv0
  `,
})``;

const FlexCenterItemsContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    flex
    justify-center
    items-center
  `,
})``;

const BlackSolutionParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    c-fluid-bk
    fw3
    f3
    lh-2
  `,
})``;

const CenteredSpacedContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    tc
    pv3
  `,
})``;

const BlackH2: StyledComponent<"h2", Record<string, unknown>> = styled.h2.attrs(
  {
    className: `
    c-fluid-bk
    fw7
    f1
    tc
  `,
  }
)``;

const RegularRedButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    outline-transparent
    bg-button-red
    hv-bg-fluid-rd
    pointer
    white
    pv3
    ph4
    fw7
    f3
    dib
    t-all-3-eio
    br2
    bc-fluid-red
    ba
  `,
})``;

const SquaredCardContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    counter-container
    bg-white
    bs-btm-h-10
    br3
    dib-l
    ph4
    mh4-l
    center
    mv0-l
    mv4
  `,
})``;

const BannerSubtitle: StyledComponent<
  "h2",
  Record<string, unknown>
> = styled.h2.attrs({
  className: `
    white
    f3-l
    f5-m
    f6
    fw4
    roboto
    tc
    ma0
  `,
})``;

export {
  ArticleContainer,
  ArticleTitle,
  BannerContainer,
  BannerSubtitle,
  BannerTitle,
  BlackBigHeader,
  BlackBigParagraph,
  BlackH2,
  BlackListItemSpaced,
  BlackSimpleParagraph,
  BlackSolutionParagraph,
  BreadcrumbContainer,
  BreadcrumbInnerContainer,
  BreadcrumbLink,
  BreadcrumbList,
  Break,
  CenteredSpacedContainer,
  CopyrightContainer,
  CopyrightParagraph,
  Flex,
  FlexCenterItemsContainer,
  FontAwesomeContainerSmall,
  FooterInfoLinksContainer,
  FooterInfoLink,
  FullWidthContainer,
  GetDemoContainer,
  GrayBigParagraph,
  GrayDash,
  HalfScreenContainer,
  HalfScreenContainerSpaced,
  PlayItButtonContainer,
  PlayItButtonImage,
  InnerFooterInfoContainer,
  InnerMainContentHome,
  MainContentHome,
  MainCoverHome,
  MainFooterInfoContainer,
  MenuButton,
  NavbarSubcategory,
  NavbarContactButton,
  NavbarContainer,
  NavbarInnerContainer,
  NavbarList,
  NavbarLoginButton,
  NavbarRegularButton,
  PageArticle,
  PageContainer,
  RegularRedButton,
  SolutionsParagraph,
  SolutionsSectionDescription,
  SolutionsSubtitle,
  SquaredCardContainer,
  SubcategoryLink,
};
