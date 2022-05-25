import styled from "styled-components";

interface ITextProps {
  fColor: string;
  fSize: string;
  fSizeM?: string;
  fSizeS?: string;
  marginBottom?: string;
  marginTop?: string;
}

const getSize = (defaultFSize: string, fSize?: string): string => {
  if (fSize === undefined) {
    return `${defaultFSize}px`;
  }

  return `${fSize}px`;
};

const getMargin = (margin?: string): string => {
  if (margin === undefined) {
    return "0";
  }

  return `${margin}rem`;
};

const Title = styled.p.attrs({
  className: `
    neue
    fw7
    lh-solid
  `,
})<ITextProps>`
  color: ${(props): string => props.fColor};
  margin-bottom: ${(props): string => getMargin(props.marginBottom)};
  margin-top: ${(props): string => getMargin(props.marginTop)};

  @media screen and (min-width: 60em) {
    font-size: ${(props): string => getSize(props.fSize)};
  }

  @media screen and (min-width: 30em) and (max-width: 60em) {
    font-size: ${(props): string => getSize(props.fSize, props.fSizeM)};
  }

  @media screen and (max-width: 30em) {
    font-size: ${(props): string => getSize(props.fSize, props.fSizeS)};
  }
`;

const Paragraph = styled.p.attrs({
  className: `
    roboto
    lh-solid
  `,
})<ITextProps>`
  color: ${(props): string => props.fColor};
  margin-bottom: ${(props): string => getMargin(props.marginBottom)};
  margin-top: ${(props): string => getMargin(props.marginTop)};

  @media screen and (min-width: 60em) {
    font-size: ${(props): string => getSize(props.fSize)};
  }

  @media screen and (min-width: 30em) and (max-width: 60em) {
    font-size: ${(props): string => getSize(props.fSize, props.fSizeM)};
  }

  @media screen and (max-width: 30em) {
    font-size: ${(props): string => getSize(props.fSize, props.fSizeS)};
  }
`;

export { Paragraph, Title };
