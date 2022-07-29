import styled from "styled-components";

interface ITableContainerProps {
  isRowFunctional: boolean;
  rowSize: "bold" | "thin";
}

const rowSizes: Record<ITableContainerProps["rowSize"], string> = {
  bold: "1rem",
  thin: "0",
};

const TableContainer = styled.div.attrs({
  className: "f6 overflow-auto",
})<ITableContainerProps>`
  background-color: #f4f4f6;
  border-radius: 4px;

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
    width: auto;
  }

  th {
    font-weight: 600;
    text-align: left;
    cursor: pointer;
    width: auto;
  }

  tr {
    cursor: ${(props): string => (props.isRowFunctional ? "pointer" : "unset")};
  }

  table {
    border-spacing: 0;
    table-layout: auto;
    width: 100%;
    margin: 16px;
  }
`;

const ToggleContainer = styled.div``;

export { ToggleContainer, TableContainer };
