import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import "./index.css";

const LoginGrid: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "br2 flex justify-center flex-column login-grid pa4",
})`
  background-color: #f4f4f6;
`;

export { LoginGrid };
