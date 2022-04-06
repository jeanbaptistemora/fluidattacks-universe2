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
  min-height: 50vh;
  background-color: #e9e9ed;
`;

const MainContentPortrait = styled.div.attrs({
  className: `
    mv5
    ph-body
    mw-1366
    center
    w-100
    flex
    flex-wrap
    justify-center
    items-center
  `,
})``;

const InnerMainContentPortrait = styled.div.attrs({
  className: `
    center
    pt0-ns
    pt4
    cf
  `,
})`
  width: 50%;
  text-align: left;

  @media (max-width: 984px) {
    width: 100%;
    text-align: center;
  }
`;

const PortraitImageContainer = styled.div.attrs({
  className: `
    fr-l
    mt3
    center
    pt0-ns
    pl3
    tc
  `,
})`
  width: 50%;

  @media (max-width: 984px) {
    width: 100%;
  }
`;

const PortraitBigParagraph = styled.p.attrs({
  className: `
    f1
    c-fluid-bk
    fw6
    neue
    lh-solid
    ma0
  `,
})``;

const PortraitParagraph = styled.p.attrs({
  className: `
    f3
    c-black-gray
    roboto
    mv4
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
