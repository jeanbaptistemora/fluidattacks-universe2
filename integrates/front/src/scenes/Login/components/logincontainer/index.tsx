import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import style from "scenes/Login/components/logincontainer/index.css";

const LoginContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `${style.container} h-100 flex items-center justify-center mv0 center overflow-y-scroll-l overflow-y-hidden-m overflow-y-hidden`,
})``;

export { LoginContainer };
