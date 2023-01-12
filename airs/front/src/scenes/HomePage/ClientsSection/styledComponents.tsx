import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    db
    tc
    pb5
    center
    ph-body
  `,
})<{ bgColor: string }>`
  background-color: ${({ bgColor }): string => bgColor};
`;

const ClientsContainer = styled.div.attrs({
  className: `
    w-100
    relative
    center
    overflow-hidden
  `,
})<{ gradientColor: string }>`
  z-index: 0;
  max-width: 1400px;

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
    width: 100px;
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
`;

const SlideShow = styled.div.attrs({
  className: `
    product-slide-track
    flex
  `,
})`
  > img {
    max-width: 135px;
    max-height: 70px;
  }
`;

export { ClientsContainer, Container, SlideShow };
