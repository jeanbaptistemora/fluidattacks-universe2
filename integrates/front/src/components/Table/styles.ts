import styled from "styled-components";

interface ITableContainerProps {
  rowSize: "bold" | "thin";
}

const rowSizes: Record<ITableContainerProps["rowSize"], string> = {
  bold: "1rem",
  thin: "0",
};

const TableContainer = styled.div.attrs({
  className: "f6 overflow-auto pa3",
})<ITableContainerProps>`
  background-color: #f4f4f6;

  td,
  th {
    border-bottom-style: solid;
    border-bottom-width: 1px;
    border-color: rgba(0, 0, 0, 0.2);
    padding-bottom: ${(props): string => rowSizes[props.rowSize]};
    padding-right: ${(props): string => rowSizes[props.rowSize]};
  }

  td {
    padding-top: ${(props): string => rowSizes[props.rowSize]};
  }

  th {
    font-weight: 600;
    text-align: left;
  }

  tr {
    cursor: pointer;
  }

  table {
    border-spacing: 0;
    table-layout: auto;
    width: 100%;
  }
`;

export { ITableContainerProps, TableContainer };
