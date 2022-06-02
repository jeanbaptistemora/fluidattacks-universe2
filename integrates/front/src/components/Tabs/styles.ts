import { NavLink } from "react-router-dom";
import styled from "styled-components";

const TabLink = styled(NavLink)`
  color: #b0b0bf;
  font-size: 20px;
  padding-bottom: 12px;
  text-decoration: none;

  &.active {
    border-bottom: 2px solid #5c5c70;
    color: #2e2e38;
  }

  :hover {
    color: #2e2e38;
  }
`;

export { TabLink };
