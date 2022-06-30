import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const Col100: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph3 w-100 relative",
})``;

const Col25: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph3 w-25 relative",
})``;

const Col33: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph3 w-33 relative",
})``;

const Col50: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "ph3 w-50 relative",
})``;

export { Col100, Col25, Col33, Col50 };
