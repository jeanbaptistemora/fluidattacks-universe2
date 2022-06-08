import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    tc
    pv5
    h-500
    bg-darker-blue
    center
  `,
})<{ bgColor: string }>`
  background-color: ${({ bgColor }): string => bgColor};
`;

const ClientsContainer = styled.div.attrs({
  className: `
    w-100
    mw-1920
    relative
    center
    overflow-hidden
  `,
})<{ gradientColor: string }>`
  z-index: 0;

  @media screen and (min-width: 30em) {
    &::before,
    &::after {
      background: linear-gradient(
        to left,
        transparent,
        ${({ gradientColor }): string => gradientColor}
      );
      content: "";
      height: 100%;
      position: absolute;
      width: 200px;
      z-index: 2;
    }

    &::after {
      right: 0;
      top: 0;
      transform: rotateZ(180deg);
    }

    &::before {
      left: 0;
      top: 0;
    }
  }
`;

const SlideShow = styled.div.attrs({
  className: `
    home-slide-track
    flex
  `,
})`
  > img {
    max-width: 382px;
    max-height: 200px;
  }
`;

export { ClientsContainer, Container, SlideShow };
