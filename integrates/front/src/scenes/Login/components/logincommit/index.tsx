import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import "./index.css";

const LoginCommit: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "absolute commit",
})``;

export { LoginCommit };
