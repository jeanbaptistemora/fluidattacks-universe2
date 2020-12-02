import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const LoginRow: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "cf pa1-ns content-center tc",
})``;

export { LoginRow };
