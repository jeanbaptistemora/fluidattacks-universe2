import _ from "lodash";
import React from "react";
import type { ColumnFormatter } from "react-bootstrap-table-next";
import { Link } from "react-router-dom";
import styled from "styled-components";

const TableLink = styled(Link)`
  border: none;
  color: #5c5c70;
  border-bottom: solid 1px;

  :hover {
    color: #2e2e38;
  }
`;

const linkFormatter = (
  callback: (cell: string, row: Record<string, string>) => string
): ColumnFormatter<Record<string, string>> => {
  const renderLink = (
    cell: string,
    row: Record<string, string>
  ): JSX.Element => {
    return <TableLink to={callback(cell, row)}>{_.capitalize(cell)}</TableLink>;
  };

  return renderLink;
};

export { linkFormatter };
