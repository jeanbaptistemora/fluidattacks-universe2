import styled from "styled-components";

const AdvisoryCardContainer = styled.div.attrs({
  className: `
    bg-white
    ma3
    pa3
    br3
  `,
})`
  width: 380px;
  @media screen and (max-width: 480px) {
    width: 100%;
  }
`;

const CardTitle = styled.p.attrs({
  className: `
    f3
    c-fluid-bk
    roboto
    b
    mt3
    mb0
  `,
})`
  min-height: 108px;
`;

const CardSubtitle = styled.p.attrs({
  className: `
    b
    f4
    roboto
    mb0
  `,
})`
  color: #787891;
`;

const CardDescriptionContainer = styled.div.attrs({
  className: `
    mv3
  `,
})``;

const CardDescription = styled.p.attrs({
  className: `
    f5
    roboto
    ma0
  `,
})`
  color: #787891;
`;

export {
  AdvisoryCardContainer,
  CardDescription,
  CardDescriptionContainer,
  CardSubtitle,
  CardTitle,
};
