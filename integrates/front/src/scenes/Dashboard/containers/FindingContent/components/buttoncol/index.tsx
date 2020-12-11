import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const ButtonCol: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "w-40 flex items-center justify-end",
})``;

export { ButtonCol };
