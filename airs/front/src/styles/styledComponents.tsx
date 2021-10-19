/* eslint import/no-namespace:0 */
import { Link } from "gatsby";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

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
    bg-gray-244
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
    flex
    flex-nowrap
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
    roboto
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
    c-black-gray
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

const BlogPageArticle: StyledComponent<
  "article",
  Record<string, unknown>
> = styled.article.attrs({
  className: `
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

const FaqContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    mw-900
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
  background-image: url("https://res.cloudinary.com/fluid-attacks/image/upload/v1619036564/airs/home/cover-main_imgm6u.webp");
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
    f1-l
    f2
    c-fluid-bk
    fw7
    tl
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
    f1-l
    f2
    c-fluid-bk
    fw6
    tl
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
    f1-l
    f2
    c-fluid-gray
    fw6
    tl
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
    bg-lightgray-xs
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

const LittleBannerTitle: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    white
    fw7
    f1
    neue
    tc
    f-375-l
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
    pv4-l
  `,
})``;

const BigPageContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    roboto
    mw-1920
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
    ph0-ns
  `,
})``;

const FullWidthContainerPlain: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
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

const SolutionCardContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pv3
    flex
    w-100
    w-50-l
    pr4-l
  `,
})``;

const SolutionsSubtitle: StyledComponent<
  "h3",
  Record<string, unknown>
> = styled.h3.attrs({
  className: `
    c-fluid-bk
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
    c-black-gray
    f5
    lh-copy
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

const LittleBlackParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    c-fluid-bk
    fw3
    f-1125
    lh-2
    mw-750
  `,
})``;

const BigSolutionParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    c-black-gray
    fw3
    f-1125
    lh-2
    mw-1920
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
    roboto
  `,
})``;

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
    f3-l
    f5-m
    f6
    fw4
    roboto
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
    f1-s
    f-375
    neue
    ml3
  `,
})``;

const MarkedTitleContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    bg-lightgray
    center
    flex
    flex-wrap
    mw-1200
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

const MarkedPhrase: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    f3
    c-black-gray
    lh-title
    normal
    roboto
    tl
    w-60-ns
  `,
})``;

const LittleBannerContainer: StyledComponent<
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
    mw-1366
    ml-auto
    mr-auto
  `,
})``;

const BlogItemTitle: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    tc
    roboto
    pv4
  `,
})``;

const BlogItemListContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    roboto
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
})``;
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
const CardFooter: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    tc
    fw3
    w-100
    pointer
    bn
    bg-white
    outline-transparent
    dn
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
    roboto
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
    roboto
    internal
    mw-1200
    center
    roboto
    bg-lightgray
    ph4-l
    ph3
    pt5-l
    pt4
    pb5
  `,
})``;

const AdvisoriesGrid: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    advisories-grid
    center
    grid
    mt4
  `,
})``;
const AdvisoriesContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    tc
    mb4
  `,
})``;

const AdvisoryContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    roboto
    internal
    internal-advisory
    mw-900
    ml-auto
    mr-auto
    bg-white
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
    roboto
    internal
    mw-900
    ml-auto
    mr-auto
    roboto
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
    roboto
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

const CompliancesGrid: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    grid
    compliance-content
    compliance-grid
    roboto
    w-100
  `,
})``;

const ComplianceContainer: StyledComponent<
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
    compliance-page
    flex
    flex-wrap
    items-center
    justify-center
  `,
})``;

const PlansCards: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    flex
    flex-wrap
    justify-center
  `,
})``;

const PlansContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    plans-feat
    roboto
    internal
    mw-1366
    ph-body
    ml-auto
    mr-auto
    roboto
    bg-white
    ph4-l
    ph3
    pt5-l
    pt4
    pb5
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
    neue
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
    neue
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
    roboto
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
    mt4
    min-h-25
  `,
})``;

const ContactButtonContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    tl
    pb3
    ph3
  `,
})``;

const ContactButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    outline-transparent
    fw7
    f-18
    br2
    bw1
    ph5
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

const BannerH2Title: StyledComponent<
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

export {
  AdvisoriesContainer,
  AdvisoriesGrid,
  AdvisoryContainer,
  ArticleContainer,
  ArticleTitle,
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
  BigSolutionParagraph,
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
  ButtonContainer,
  CardBody,
  CardContainer,
  CardFooter,
  CardHeader,
  CardReadMore,
  CardsContainer,
  CardsContainer1200,
  CenteredSpacedContainer,
  ComplianceContainer,
  CompliancesGrid,
  ContactButton,
  ContactButtonContainer,
  ContentContainer,
  ContentList,
  CopyrightContainer,
  CopyrightParagraph,
  ErrorContainer,
  ErrorDescription,
  ErrorSection,
  ErrorTitle,
  FaqContainer,
  Flex,
  FlexCenterItemsContainer,
  FontAwesomeContainerSmall,
  FooterInfoLinksContainer,
  FooterInfoLink,
  FullWidthContainer,
  FullWidthContainerPlain,
  GetDemoContainer,
  GrayBigParagraph,
  GrayDash,
  HalfScreenContainer,
  HeaderContainer,
  IframeContainer,
  InnerContentList,
  InnerListContainer,
  InnerListItem,
  ListItem,
  ListItemLabel,
  LittleBannerContainer,
  LittleBannerTitle,
  LittleBlackParagraph,
  LogoContainer,
  PlayItButtonContainer,
  CenteredMaxWidthContainer,
  InnerMainContentHome,
  MainContentHome,
  MainCoverHome,
  MainFooterInfoContainer,
  MarkedPhrase,
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
  PageArticle,
  PageContainer,
  PlansCards,
  PlansContainer,
  RadioButton,
  RadioLabel,
  RedMark,
  RegularRedButton,
  SidebarContainer,
  SocialMediaLink,
  SolutionCardContainer,
  SolutionsParagraph,
  SolutionsSectionDescription,
  SolutionsSubtitle,
  SquaredCardContainer,
  SubcategoryLink,
};
