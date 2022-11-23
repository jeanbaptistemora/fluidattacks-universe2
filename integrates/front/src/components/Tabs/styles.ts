import { NavLink } from "react-router-dom";
import styled from "styled-components";

const TabLink = styled(NavLink)`
  background-color: #f4f4f6;
  border: 1px solid #d2d2da;
  color: #2e2e38;
  display: inline-block;
  font-size: 16px;
  padding: 10px 16px;
  transition: all 0.3s ease;

  :hover {
    background-color: #d2d2da;
  }

  &.active {
    background-color: #2e2e38;
    border-color: #121216;
    color: #e9e9ed;

    :hover {
      background-color: #49495a;
      border-color: #2e2e38;
    }
  }
`;

export { TabLink };
