import styled from "styled-components";

const PlayButtonContainer = styled.div.attrs({
  className: `
    fl
    flex
    relative
    pointer
  `,
})`
  width: 64px;
  height: 64px;
  top: 65%;
  left: 25px;
  z-index: 1;

  @media screen and (max-width: 480px) {
    top: 50%;
  }
`;

const PlayImageContainer = styled.div.attrs({
  className: `
    dib
    center
    relative
  `,
})`
  > div + img {
    margin-top: -64px;
  }
`;

const HomeVideoContainer = styled.div.attrs({
  className: `
    w-100
    w-40-l
    relative
  `,
})<{ isVisible: boolean }>`
  display: ${({ isVisible }): string => (isVisible ? "block" : "none")};

  iframe {
    width: 100%;
    height: 341px;
  }
`;

const HomeImageContainer = styled.div.attrs({
  className: `
    w-100
    w-40-l
    relative
  `,
})<{ isVisible: boolean }>`
  display: ${({ isVisible }): string => (isVisible ? "none" : "flex")};
`;

const MainCoverHome = styled.div.attrs({
  className: `
    flex
    items-center
    cover-m
    cover-s
    bg-banner-sz
  `,
})`
  background-image: url("https://res.cloudinary.com/fluid-attacks/image/upload/v1643995540/airs/home/dark-cover-main.webp");
  min-height: 100vh;
`;

const MainContentHome = styled.div.attrs({
  className: `
    pv5
    flex
    w-100
    center
    mw-1366
    ph-body
    flex-wrap
    items-center
  `,
})`
  direction: rtl;
`;

const TextContainer = styled.div.attrs({
  className: `
    tl
    w-60-l
    w-100
  `,
})``;

export {
  HomeImageContainer,
  HomeVideoContainer,
  MainContentHome,
  MainCoverHome,
  PlayButtonContainer,
  PlayImageContainer,
  TextContainer,
};
