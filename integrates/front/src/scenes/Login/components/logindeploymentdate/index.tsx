import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import "./index.css";

const LoginDeploymentDate: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "absolute deployment-date",
})``;

export { LoginDeploymentDate };
