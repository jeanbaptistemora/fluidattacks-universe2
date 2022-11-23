import styled from "styled-components";

const ButtonGroup = styled.div.attrs({
  className: "comp-button-group",
})`
  .comp-button:not(:first-child) {
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
  }
  .comp-button:not(:last-child) {
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
  }
`;

export { ButtonGroup };
