import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    bg-white
    flex
    ph-body
  `,
})``;

const CardContainer = styled.div.attrs({
  className: `
    br2
    ba
    pv5
    ph4
    mv5
    ph6-l
    w-100
    center
    mw-1366
  `,
})`
  border-color: #ff3435;
  box-shadow: 0px 0px 6px 3px rgb(0 0 0 / 8%);
`;

const CardButton = styled.div.attrs({
  className: `
    flex
    items-center
    t-all-3-eio
  `,
})`
  > p {
    transition: all 0.3s ease-in-out;
  }

  > p + svg {
    color: #ff3435;
    font-size: 36px;
  }

  :hover > p {
    color: #ff3435;
    margin-right: 5px;
  }
`;

export { CardContainer, CardButton, Container };
