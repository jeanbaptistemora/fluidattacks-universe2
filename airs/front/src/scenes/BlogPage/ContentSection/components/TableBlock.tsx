import React from "react";

import { TableBlockContainer } from "./styledComponents";

import { Container } from "../../../../components/Container";

interface ITableBlock {
  children: React.ReactNode;
}

const TableBlock: React.FC<ITableBlock> = ({ children }): JSX.Element => (
  <Container borderColor={"#f4f4f6"} br={3} ph={3} pv={3} shadow={true}>
    <TableBlockContainer>{children}</TableBlockContainer>
  </Container>
);

export { TableBlock };
