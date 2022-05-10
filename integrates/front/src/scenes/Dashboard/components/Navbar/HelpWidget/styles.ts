import styled from "styled-components";

const Button = styled.button.attrs({
  className:
    "bn br3 br--top gray hover-bg-light-silver outline-0 ph3 pv2 pointer tl w-100",
})`
  background: none;
  & svg {
    margin-right: 5px;
  }
`;
const ExtraMessage = styled.div.attrs({
  className: "mid-gray pb2 pt2 pl3 pr3",
})``;
const Message = styled.div.attrs({
  className: "b--mid-light-gray bg-lbl-gray br3 f6 ml2 mb3 outline-transparent",
})``;

export { Button, ExtraMessage, Message };
