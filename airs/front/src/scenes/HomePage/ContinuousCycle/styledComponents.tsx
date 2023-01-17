import styled from "styled-components";

const SlideShow = styled.div.attrs({
  className: `
    flex
    overflow-hidden-l
    overflow-x-auto
    scroll-smooth
    center
  `,
})`
  width: 100%;
`;

const SlideHook = styled.div.attrs({
  className: `
    flex
    scroll-smooth
  `,
})`
  width: 0%;
`;

const ProgressBar = styled.div.attrs({
  className: `
    relative
  `,
})<{ width: string }>`
  background-color: #bf0b1a;
  height: ${({ width }): string => width};
  width: 4px;
  transition: width 0.25s;
`;

export { SlideShow, SlideHook, ProgressBar };
