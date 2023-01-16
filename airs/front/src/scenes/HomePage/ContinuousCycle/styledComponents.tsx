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

export { SlideShow };
