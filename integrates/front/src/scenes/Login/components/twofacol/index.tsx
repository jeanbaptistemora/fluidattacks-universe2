import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const TwoFacol: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "w-33 pa1",
})``;

export { TwoFacol };
