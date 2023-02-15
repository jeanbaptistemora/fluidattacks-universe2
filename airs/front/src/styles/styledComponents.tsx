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
    bg-gray-244
  `,
})<{ isScrolled: boolean }>`
  position: sticky;
  border-radius: ${({ isScrolled }): string => (isScrolled ? "2px" : "none")};
  box-shadow: ${({ isScrolled }): string =>
    isScrolled ? "0px 1px 10px #999" : "none"};
`;

const NavbarInnerContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    b
    relative
    w-100
    z-5
    mr-auto
    ml-auto
    h-navbar
  `,
})`
  max-width: 1266px;
`;

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
    flex
    flex-nowrap
    items-center
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
    db
    dn
  `,
})``;

const NavbarContactButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    outline-transparent
    fw5
    f-18
    br2
    bw1
    ph3
    pv2
    bg-fluid-red
    bc-hovered-red
    ba
    hv-bg-fluid-dkred
    hv-bd-fluid-dkred
    t-all-3-eio
    white
    pointer
  `,
})``;

const MobileContactButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    outline-transparent
    fw5
    f4
    br2
    bw1
    ph3
    bg-fluid-red
    bc-hovered-red
    ba
    hv-bg-fluid-dkred
    hv-bd-fluid-dkred
    t-all-3-eio
    white
    pointer
    mb3
    w-90
    pv3
    justify-center
    flex
    center
    mh3
  `,
})``;

const NavbarItem = styled.li.attrs<{ className: string }>({
  className: `
    mr3
    pr2
    pv4
  `,
})``;

const NavbarLoginButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    outline-transparent
    fw5
    f-18
    br2
    bw1
    ph3
    pv2
    bg-gray-233
    bc-gray-233
    ba
    hv-bg-soft-gray
    hv-bd-soft-gray
    t-all-3-eio
    c-black-gray
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
    c-fluid-bk
  `,
})``;

const NavbarSubcategory: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    poppins
    mt4
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
    c-fluid-gray
    b
    f6
    fw2
    poppins
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
    w-100
    center
  `,
})``;

const CenteredMaxWidthContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    mw-1366
    ph-body
    center
  `,
})``;

const CopyrightContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    tc
    nb3
    justify-center
  `,
})``;

const FooterInfoLinksContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h2
    b
    tc
    pv3
    justify-center
  `,
})``;

const FooterInfoLink: StyledComponent<
  "a",
  Record<string, unknown>
> = styled.a.attrs({
  className: `
    c-black-gray
    f6
    fw2
    mt2
    poppins
    no-underline
    hv-fluid-dkred
  `,
})``;

const GrayDash: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: `
    c-black-gray
    f6
  `,
})``;

const Badge = styled.span.attrs({
  className: `
    f7
    br4
    pv2
    ph3
    ma0
    poppins
  `,
})<{ bgColor: string; color: string }>`
  background-color: ${({ bgColor }): string => bgColor};
  color: ${({ color }): string => color};
`;

const PageArticle = styled.article<{ bgColor: string }>`
  background-color: ${({ bgColor }): string => `${bgColor}`};
`;

const InternalContainer = styled.article.attrs({
  className: `
    internal
  `,
})``;

const BlogPageArticle: StyledComponent<
  "article",
  Record<string, unknown>
> = styled.article.attrs({
  className: `
    pt5
    bg-gray-221
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
    poppins
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
    poppins
    ph4-l
    ph3
    pt5-l
    pt4
    pb5
  `,
})``;

const CareersFaqContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    mw-900
    ph-body
    center
    poppins
    ph4-l
    ph3
    pt5-l
    pt4
    pb5
  `,
})``;

const FaqContainer = styled.div.attrs({
  className: `
    ph-body
    center
    poppins
    bg-gray-244
    ph4-l
    ph3
    pt5-l
    pt4
    pb5
    faq-container
  `,
})`
  max-width: 950px;
  color: #5c5c70;

  a {
    color: #5c5c70;
  }
`;

const IconContainerSmall: StyledComponent<
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
    poppins
    tc
    ma0
  `,
})``;

const PageContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    poppins
    mw-1366
    ph-body
    center
    c-lightblack
    pv4-l
  `,
})``;

const BigPageContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    poppins
    mw-1920
    ph-body
    center
    c-lightblack
    pv5
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
    f2
    tc
  `,
  }
)``;

const NewRegularRedButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    outline-transparent
    bg-fluid-red
    bc-hovered-red
    hv-bg-fluid-dkred
    hv-bd-fluid-dkred
    pointer
    white
    f5
    dib
    t-all-3-eio
    br2
    bc-fluid-red
    ba
    poppins
    justify-center
    bw1
  `,
})`
  padding: 10px 16px;
`;

const PhantomRegularRedButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    outline-transparent
    bg-transparent
    bc-hovered-red
    hv-bg-fluid-rd
    pointer
    c-dkred
    f5
    dib
    t-all-3-eio
    br2
    ba
    poppins
    justify-center
    bw1
  `,
})`
  padding: 10px 16px;

  :hover {
    color: white;
  }
`;

const SquaredCardContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    counter-container
    bs-btm-h-10
    br3
    dib
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
    f5
    fw4
    poppins
    tc
    ma0
  `,
})``;

const SocialMediaLink: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    pa2
    ba
    br3
    bg-transparent
    pointer
    bc-fluid-gray
    mh1
  `,
})``;

const MarkedTitle: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    c-fluid-bk
    f1-ns
    f2
    poppins
    ml3
  `,
})``;

const MarkedTitleContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    center
    flex
    flex-wrap
    mw-900
  `,
})``;

const RedMark: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    bl-red
  `,
})``;

const BlogItemTitle: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    tc
    poppins
    pv4
  `,
})``;

const BlogItemListContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    poppins
    ml6-l
    ml4-m
  `,
})``;

const BlogItemList: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
    three-columns-l
    two-columns-m
  `,
})``;

const BlogItemItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
    pv2
  `,
})``;

const BlogItemName: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    di
    ttc
  `,
})``;

const CardsContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    cardgrid
    flex-ns
    flex-wrap-ns
    justify-around
  `,
})``;

const CardContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    br3
    bs-btm-h-10
    hv-card
    relative
    dt-ns
    mv3
    mh2
    bg-white
    w-clients-card
  `,
})`
  height: 390px;
`;

const CardHeader: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    accordion
    pointer
    pa3
    w-100
    bg-white
    outline-transparent
    bn
    t-all-5
  `,
})``;

const CardReadMore: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    absolute
    bottom-0
    right-0
    left-0
    fw3
    fadein
  `,
})``;

const CardBody: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    panel
    pv0
    ph2
    bg-white
    t-all-5
    overflow-hidden
    ph4
  `,
})``;

const MenuItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
    ph3
    pv1
    dib
    bg-lightergray
    mh2
    mt2
    br4
    hv-bg-fluid-gray
  `,
})``;

const RadioButton: StyledComponent<
  "input",
  Record<string, unknown>
> = styled.input.attrs({
  className: `
    op7
    dn
    transparent
  `,
  type: `radio`,
})``;

const RadioLabel: StyledComponent<
  "label",
  Record<string, unknown>
> = styled.label.attrs({
  className: `
    c-black-gray
    f4-ns
    f5
    poppins
    no-underline
    fw3
    hv-fluid-black
    pointer
  `,
})``;

const IframeContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    center
    overflow-x-auto
  `,
})``;

const CardsContainer1200: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    poppins
    internal
    mw-1200
    center
    poppins
    ph4-l
    ph3
    pt5-l
    pt4
    pb5
  `,
})``;

const AdvisoriesContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    mw-1200
    center
    tc
    pb4
    ph-body
  `,
})``;

const AdvisoryContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    poppins
    internal
    internal-advisory
    mw-900
    ml-auto
    mr-auto
    ph4-l
    ph3
    pt5-l
    pt4
    pb5
  `,
})``;

const BlogArticleBannerContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    coverm
    cover-s
    h-auto
    justify-center
    items-center
    flex
    bg-center
    mw-900
    ml-auto
    mr-auto
  `,
})``;
const BlogArticleContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    poppins
    internal
    mw-900
    ml-auto
    mr-auto
    poppins
    bg-white
    ph4-l
    ph3
    pt4
    pb5
  `,
})``;
const BlogArticleTitle: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    poppins
    tc
  `,
})``;
const BlogArticleSubtitle: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: `
    db
    tc c-fluid-bk
    b
    f3
    mt0
  `,
})``;

const ComplianceContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    poppins
    mw-1366
    ph-body
    center
    c-lightblack
    pv5
    compliance-page
    flex
    flex-wrap
    items-center
    justify-center
  `,
})``;

const ErrorSection: StyledComponent<
  "section",
  Record<string, unknown>
> = styled.section.attrs({
  className: `
    error-bg
    vh-100
    w-100
    cover
    bg-top
    flex
    items-center
    justify-center
  `,
})``;

const ErrorContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    flex
    flex-column
    justify-between
  `,
})``;

const ErrorTitle: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    poppins
    c-fluid-bk
    f-error
    fw7
    tc
    lh-solid
    ma0
  `,
})``;

const ErrorDescription: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    poppins
    c-fluid-bk
    f2
    fw7
    tc
    ma0
  `,
})``;

const ButtonContainer: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    tc
    mt3
  `,
})``;

const SidebarContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    bg-whitergray
    overflow-y-auto
    nowrap
  `,
})``;

const HeaderContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    flex
  `,
})``;

const LogoContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    tl
    pa4
    w-50
  `,
})``;

const ContentContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    overflow-y-auto
    w-60-m
    center
  `,
})``;

const ContentList: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
    list
    ma0
    pa0
    tl
  `,
})``;

const MenuLinksContainer = styled.div.attrs({
  className: `
    flex-m
    mh3
  `,
})``;

const ListItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
    db
    pb3
    mh3
    mobileMenuItem
    mb3
  `,
})``;

const ListItemLabel: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pointer
    hv-fluid-rd
    f3
    c-fluid-bk
    fw4
    t-color-2
    poppins
  `,
})``;

const InnerListContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pv2
  `,
})`
  display: none;
`;

const InnerContentList: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
    list
    pl3
  `,
})``;

const InnerListItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
    pv2
  `,
})``;

const MobileFooterContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    tc-m
    db
    mh3
    mt3
    min-h-25
  `,
})``;

const BannerH2Title: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    white
    fw7
    f1
    poppins
    tc
    ma0
  `,
})``;

const MenuList: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
    list
    ph0-ns
    ph3
    ma0
    tc
    pv3
    slide-show
  `,
})``;

const ServicesHeaderContainer = styled.div.attrs({
  className: `
    center
  `,
})`
  max-width: 1000px;
`;

const ServicesGrid = styled.div.attrs({
  className: `
    flex
    center
    flex-wrap
    services-benefits
  `,
})`
  max-width: 1000px;
`;

const SectionContainer = styled.div.attrs({
  className: `
    tc
    pv5
    ph-body
  `,
})``;

const SystemsCardContainer = styled.div.attrs({
  className: `
    tl
    pv5
    ph4
    w-100
    w-50-l
  `,
})``;

export {
  AdvisoriesContainer,
  AdvisoryContainer,
  ArticleContainer,
  ArticleTitle,
  Badge,
  BlogArticleBannerContainer,
  BlogArticleContainer,
  BlogArticleSubtitle,
  BlogArticleTitle,
  BlogItemName,
  BlogItemItem,
  BlogItemList,
  BlogItemListContainer,
  BlogItemTitle,
  BlogPageArticle,
  BannerContainer,
  BannerH2Title,
  BannerSubtitle,
  BannerTitle,
  BigPageContainer,
  BlackH2,
  ButtonContainer,
  CardBody,
  CardContainer,
  CardHeader,
  CardReadMore,
  CardsContainer,
  CardsContainer1200,
  CareersFaqContainer,
  CenteredSpacedContainer,
  ComplianceContainer,
  ContentContainer,
  ContentList,
  CopyrightContainer,
  CopyrightParagraph,
  ErrorContainer,
  ErrorDescription,
  ErrorSection,
  ErrorTitle,
  FaqContainer,
  FlexCenterItemsContainer,
  IconContainerSmall,
  FooterInfoLinksContainer,
  FooterInfoLink,
  FullWidthContainer,
  GrayDash,
  HeaderContainer,
  IframeContainer,
  InnerContentList,
  InnerListContainer,
  InnerListItem,
  InternalContainer,
  ListItem,
  ListItemLabel,
  LogoContainer,
  CenteredMaxWidthContainer,
  MainFooterInfoContainer,
  MarkedTitleContainer,
  MarkedTitle,
  MenuButton,
  MenuItem,
  MenuList,
  MobileContactButton,
  MobileFooterContainer,
  MenuLinksContainer,
  NavbarSubcategory,
  NavbarContactButton,
  NavbarContainer,
  NavbarItem,
  NavbarInnerContainer,
  NavbarList,
  NavbarLoginButton,
  NavbarRegularButton,
  NewRegularRedButton,
  PageArticle,
  PageContainer,
  PhantomRegularRedButton,
  RadioButton,
  RadioLabel,
  RedMark,
  SectionContainer,
  ServicesHeaderContainer,
  ServicesGrid,
  SidebarContainer,
  SocialMediaLink,
  SquaredCardContainer,
  SubcategoryLink,
  SystemsCardContainer,
};
