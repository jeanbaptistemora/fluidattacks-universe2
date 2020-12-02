import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const LoginContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "items-center flex flex-row white h-100",
})``;

export { LoginContainer };
