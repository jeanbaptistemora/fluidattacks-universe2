import styled from "styled-components";

import { MenuDivider } from "./MenuDivider";
import { MenuItem } from "./MenuItem";

interface IMenuProps {
  align: "left" | "right";
}

const Menu = styled.ul.attrs({
  className: "absolute f5 list mt3 ph0 pv2 shadow-1",
})<IMenuProps>`
  background-color: #f4f4f6;
  left: auto;
  max-width: 400px;
  min-width: 240px;
  right: ${(props): string => (props.align === "right" ? "0" : "unset")};
`;

export { Menu, MenuDivider, MenuItem };
