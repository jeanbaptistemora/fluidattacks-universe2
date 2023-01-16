import styled, { keyframes } from "styled-components";

const SolutionAnimation = keyframes`
  0% { transform: translateX(0); }
  100% { transform: translateX(calc(-330px * 8));}
  `;

const CardFooter = styled.div`
  margin-top: auto;
`;

const MainCoverHome = styled.div.attrs({
  className: `
    flex
    cover-m
    cover-s
    bg-banner-sz
  `,
})`
  background-image: url("https://res.cloudinary.com/fluid-attacks/image/upload/v1673463494/airs/home/Solutions/solutions-bg.webp");
`;

const SolutionsContainer = styled.div.attrs({
  className: `
  flex
  wrap
    w-100
    relative
    center
    overflow-hidden
  `,
})<{ gradientColor: string }>`
  z-index: 0;
  max-width: 1600px;
  margin-bottom: 90px;

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
    flex
  `,
})`
  animation: ${SolutionAnimation} 100s linear infinite;
  width: calc(330px * 8);
  &:hover {
    animation-play-state: paused;
  }
  > div {
    margin-left: 30px;
    margin-top: 30px;
    min-width: 300px;
    max-width: 300px;
    max-height: 318px;
  }
`;

export { CardFooter, MainCoverHome, SolutionsContainer, SlideShow };
