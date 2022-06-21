import { NavLink } from "react-router-dom";
import styled from "styled-components";

const TabLink = styled(NavLink)`
  box-sizing: border-box;
  color: #b0b0bf;
  display: block;
  font-size: 20px;
  padding: 8px;
  text-decoration: none;

  &.active {
    border-bottom: 2px solid #5c5c70;
    color: #2e2e38;
  }

  :hover {
    color: #49495a;
  }
`;

export { TabLink };
