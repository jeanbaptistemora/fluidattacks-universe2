import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import "./index.css";

const LoginGrid: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "login-grid center pa2",
})``;

export { LoginGrid };
