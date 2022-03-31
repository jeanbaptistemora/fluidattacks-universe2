import styled from "styled-components";

const BigRegularRedButton = styled.button.attrs({
  className: `
    outline-transparent
    bg-fluid-red
    pointer
    white
    pv3
    ph4
    fw7
    f3
    dib
    t-all-3-eio
    br2
    bc-fluid-red
    ba
    roboto
    w-auto-ns
    w-100
  `,
})`
  :hover {
    background-color: #b80000;
    box-shadow: 0px 15px 23px rgba(255, 52, 53, 0.3);
  }
`;

export { BigRegularRedButton };
