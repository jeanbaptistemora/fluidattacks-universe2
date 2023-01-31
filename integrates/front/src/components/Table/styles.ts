import { Link } from "react-router-dom";
import styled from "styled-components";

interface ITableContainerProps {
  clickable: boolean;
}

const TableContainer = styled.div.attrs({
  className: "f6 overflow-auto",
})<ITableContainerProps>`
  background-color: #f4f4f6;
  border: solid 1px #d2d2da;
  border-radius: 4px;
  margin-top: 8px;

  table {
    border-spacing: 0;
    padding: 12px;
    table-layout: auto;
    width: 100%;
  }

  td,
  th {
    border-bottom: solid 1px #8888;
    padding: 12px;
    width: auto;
    white-space: pre-line;
  }

  tr {
    cursor: ${({ clickable }): string => (clickable ? "pointer" : "unset")};

    &:last-child > td {
      border: none;
    }
  }

  label > input,
  div {
    cursor: ${({ clickable }): string => (clickable ? "pointer" : "unset")};
  }

  th {
    cursor: pointer;
    font-weight: 700;
    text-align: left;
  }
`;

const TableLink = styled(Link)`
  border: none;
  border-bottom: solid 1px;
  color: #5c5c70;

  :hover {
    color: #2e2e38;
  }
`;

const ToggleContainer = styled.div``;

export { TableLink, ToggleContainer, TableContainer };
