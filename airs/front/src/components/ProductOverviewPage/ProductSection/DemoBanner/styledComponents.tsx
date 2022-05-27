import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    center
    flex
    bg-white
    items-center
    mv5
  `,
})``;

const TextContainer = styled.div.attrs({
  className: `
    w-50
    tl
  `,
})``;

const ImageContainer = styled.div.attrs({
  className: `
    w-50
    flex
    relative
  `,
})<{ margin: boolean }>`
  margin-left: ${({ margin }): string => (margin ? "3rem" : "unset")};
  margin-right: ${({ margin }): string => (margin ? "unset" : "3rem")};
`;

export { Container, ImageContainer, TextContainer };
