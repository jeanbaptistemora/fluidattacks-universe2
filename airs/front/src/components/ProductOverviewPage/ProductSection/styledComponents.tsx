import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    flex
    flex-nowrap-l
    flex-wrap
    center
    ph-body
    bg-white
    justify-center
  `,
})``;

const SectionContainer = styled.div.attrs({
  className: `
    flex
    db-l
    flex-wrap-l
    product-section
    overflow-x-auto
  `,
})`
  -ms-overflow-style: none;
  scrollbar-width: none;

  ::-webkit-scrollbar {
    display: none;
  }
`;

const ProgressCol = styled.div.attrs({
  className: `
    dn
    mr4
    mv6
    db-l
    relative
  `,
})``;

const ProgressContainer = styled.div.attrs({
  className: `
    absolute
  `,
})`
  width: 3px;
  height: 90%;
  background-color: #f4f4f6;
`;

const ProgressBar = styled.div.attrs({
  className: `
    w-100
    absolute
  `,
})`
  transition: height 0.25s;
  background-color: #d2d2da;
`;

const HorizontalProgressContainer = styled.div.attrs({
  className: `
    w-100
    mt4
    mb5
    dn-l
    relative
  `,
})`
  height: 3px;
  background-color: #f4f4f6;
`;

const HorizontalProgressBar = styled.div.attrs({
  className: `
    h-100
    absolute
  `,
})`
  transition: width 0.25s;
  background-color: #d2d2da;
`;

export {
  Container,
  HorizontalProgressBar,
  HorizontalProgressContainer,
  ProgressBar,
  ProgressCol,
  ProgressContainer,
  SectionContainer,
};
