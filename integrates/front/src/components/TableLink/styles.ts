import { Link } from "react-router-dom";
import styled from "styled-components";

const TableLinkButton = styled(Link)<{ isNone: boolean }>`
  border: none;
  color: #5c5c70;
  opacity: ${({ isNone }): string => (isNone ? "50%" : "100%")};
  border-bottom: ${({ isNone }): string => (isNone ? "0" : "solid 1px")};

  :hover {
    color: #2e2e38;
  }
`;

export { TableLinkButton };
