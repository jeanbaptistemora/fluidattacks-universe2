import styled from "styled-components";

const Field = styled.p.attrs({ className: "ma0 pv1" })``;

const Label = styled.span`
  :after {
    content: ": ";
  }
`;

export { Field, Label };
