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
    f4
    c-fluid-bk
    roboto
    b
    mt3
    mb0
  `,
})`
  min-height: 60px;
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

const AdvisoriesGrid = styled.div.attrs({
  className: `
    flex
    mt4
    flex-wrap
    justify-center
    center
  `,
})`
  max-width: 1300px;
`;

export {
  AdvisoriesGrid,
  AdvisoryCardContainer,
  CardDescription,
  CardDescriptionContainer,
  CardSubtitle,
  CardTitle,
};
