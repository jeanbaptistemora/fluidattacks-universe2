import styled from "styled-components";

const PortraitContainer = styled.div.attrs({
  className: `
    flex
    items-center
    cover-m
    cover-s
    bg-banner-sz
  `,
})`
  background-image: url("https://res.cloudinary.com/fluid-attacks/image/upload/v1648748426/airs/product-overview/portrait/cover-portrait.webp");
  min-height: 50vh;

  @media (max-width: 480px) {
    background-image: unset;
    background-color: #e9e9ed;
  }
`;

const MainContentPortrait = styled.div.attrs({
  className: `
    mv5
    ph-body
    mw-1366
    center
    w-100
  `,
})``;

const InnerMainContentPortrait = styled.div.attrs({
  className: `
    fl-l
    w-100
    w-50-l
    center
    pt0-ns
    pt4
    cf
    tl
  `,
})``;

const PortraitImageContainer = styled.div.attrs({
  className: `
    fr-l
    w-100
    w-50-l
    mt3
    center
    pt0-ns
    pl3
    tc
  `,
})``;

const PortraitBigParagraph = styled.p.attrs({
  className: `
    f1
    c-fluid-bk
    fw6
    tl
    neue
    lh-solid
    ma0
    tl-l
    tc
  `,
})``;

const PortraitParagraph = styled.p.attrs({
  className: `
    f3
    c-black-gray
    roboto
    mv4
    tl-l
    tc
  `,
})`
  line-height: 2rem;
`;

export {
  InnerMainContentPortrait,
  MainContentPortrait,
  PortraitBigParagraph,
  PortraitContainer,
  PortraitImageContainer,
  PortraitParagraph,
};
