import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    pv5
    ph-body
    flex-wrap
  `,
})`
  background-color: #2e2e38;
`;

const CardContainer = styled.div.attrs({
  className: `
    tc
    pv5
    ph4
    br2
    center
  `,
})`
  max-width: 1135px;
  background-color: #ffffff;
  box-shadow: 0px 0px 6px 3px rgba(0, 0, 0, 0.06);
`;

export { CardContainer, Container };
