import styled from "styled-components";

const Button = styled.a`
  border: none;
  color: #5c5c70;
  opacity: 100%;
  border-bottom: solid 1px;

  :hover {
    color: #2e2e38;
  }
`;

const SortsSuggestionsButton = styled(Button)<{ isNone: boolean }>`
  opacity: ${({ isNone }): string => (isNone ? "50%" : "100%")};
  border-bottom: ${({ isNone }): string => (isNone ? "0" : "solid 1px")};
  cursor: ${({ isNone }): string => (isNone ? "default" : "pointer")};
`;

const Field = styled.p.attrs({ className: "ma0 pv1" })``;

const Label = styled.span`
  :after {
    content: ": ";
  }
`;

const Value = styled.span.attrs({
  className: "f5 lh-title ma0 pr1-l ws-pre-wrap gray",
})``;

export { SortsSuggestionsButton, Field, Label, Value };
