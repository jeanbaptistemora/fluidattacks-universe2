import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const StyledInputContainer = styled.div`
  width: fit-content;
  border: 1px solid #d2d2da;
  border-radius: 0;
  background: none;
  color: #2e2e38;
  font-family: Roboto, sans-serif;
  font-size: 16px;
`;

const StyledInput = styled.input`
  width: 4em;
  border-style: none;
  padding: 0.5rem;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  padding-left: 0.5rem;
  background: none;

  &:focus {
    border-color: none;
    box-shadow: none;
    outline: none;
  }

  ::-webkit-outer-spin-button,
  ::-webkit-inner-spin-button {
    appearance: none;
    margin: 0;
  }
`;

const Col50: StyledComponent<"div", Record<string, unknown>> = styled.div`
  width: auto;
  padding: 0.5em;
  text-align: center;
`;

const Row: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "flex",
})``;

const VerticalLine = styled.div`
  border-left: 1px solid #d2d2da;
  height: 30px;
`;

const StyledFontAwesomeIcon = styled(FontAwesomeIcon)`
  &:focus {
    border-color: none;
    box-shadow: none;
    outline: none;
  }
`;

export {
  StyledInputContainer,
  StyledInput,
  Col50,
  Row,
  VerticalLine,
  StyledFontAwesomeIcon,
};
