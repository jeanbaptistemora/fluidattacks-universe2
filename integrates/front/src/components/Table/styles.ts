import styled from "styled-components";

interface ITableContainerProps {
  rowSize: "bold" | "thin";
}

interface IRowSize {
  paddingBottom: string;
  paddingRight: string;
  paddingTop: string;
}

const rowSizes: Record<ITableContainerProps["rowSize"], IRowSize> = {
  bold: {
    paddingBottom: "1rem",
    paddingRight: "1rem",
    paddingTop: "1rem",
  },
  thin: {
    paddingBottom: "0",
    paddingRight: "0",
    paddingTop: "0",
  },
};

const TableContainer = styled.div.attrs({
  className: "pa3 w-100",
})<ITableContainerProps>`
  background-color: #f4f4f6;

  th,
  td {
    border-bottom-style: solid;
    border-bottom-width: 1px;
    border-color: rgba(0, 0, 0, 0.2);
    padding-bottom: ${(props): string => rowSizes[props.rowSize].paddingBottom};
    padding-right: ${(props): string => rowSizes[props.rowSize].paddingRight};
  }

  th {
    font-weight: 600;
    text-align: left;
  }

  td {
    padding-top: ${(props): string => rowSizes[props.rowSize].paddingTop};
  }
`;

export { ITableContainerProps, TableContainer };
