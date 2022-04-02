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
    f3-ns
    f4
    dib
    t-all-3-eio
    br2
    ba
    roboto
    w-auto-ns
    w-100
  `,
})`
  border-color: #ff3435;
  :hover {
    background-color: #b80000;
  }
`;

export { BigRegularRedButton };
