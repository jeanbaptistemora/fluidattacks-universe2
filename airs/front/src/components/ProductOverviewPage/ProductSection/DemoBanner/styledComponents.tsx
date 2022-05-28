import styled from "styled-components";

const BannerContainer = styled.div.attrs({
  className: `
    center
    flex-l
    dn
    items-center
    mv5
  `,
})`
  max-width: 1400px;
`;

const CardContainer = styled.div.attrs({
  className: `
    mv5
    mh4
    dn-l
    flex
    flex-wrap
  `,
})`
  @media (max-width: 960px) {
    min-width: 500px;
  }
  @media (max-width: 700px) {
    min-width: 300px;
  }
  @media (max-width: 500px) {
    min-width: 200px;
  }
`;

const TextContainer = styled.div.attrs({
  className: `
    w-50-l
    w-100
    tl
  `,
})``;

const ImageContainer = styled.div.attrs({
  className: `
    w-50-l
    w-100
    flex
    relative
  `,
})<{ margin: boolean }>`
  margin-right: auto;
  margin-left: auto;

  @media (min-width: 960px) {
    margin-left: ${({ margin }): string => (margin ? "3rem" : "unset")};
    margin-right: ${({ margin }): string => (margin ? "unset" : "3rem")};
  }
`;

export { BannerContainer, CardContainer, ImageContainer, TextContainer };
