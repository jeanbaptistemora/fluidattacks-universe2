import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    flex
    center
    ph-body
    bg-white
    justify-center
    product-section
  `,
})``;

const SectionContainer = styled.div.attrs({
  className: `
    flex
    db-l
    flex-wrap-l
    overflow-x-auto
  `,
})``;

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
})<{ height: string }>`
  height: ${({ height }): string => height}%;
  transition: height 0.25s;
  background-color: #d2d2da;
`;

export {
  Container,
  ProgressBar,
  ProgressCol,
  ProgressContainer,
  SectionContainer,
};
