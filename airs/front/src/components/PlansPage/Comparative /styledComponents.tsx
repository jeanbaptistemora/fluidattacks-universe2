import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    tc
    ph-body
    pv5
  `,
})`
  background-color: #f4f4f6;
`;

const TableDescription = styled.div.attrs({
  className: `
    tl
    mt3
    center
    mw-1366
  `,
})``;

const TableContainer = styled.div.attrs({
  className: `
    center
    overflow-x-auto
    mw-1366
  `,
})`
  ::-webkit-scrollbar {
    width: 3px;
  }

  ::-webkit-scrollbar-track {
    background: #e9e9ed;
  }

  ::-webkit-scrollbar-thumb {
    background: #d2d2da;
  }
`;

const BoldColor = styled.span.attrs({
  className: `
    b
  `,
})<{ fColor: string }>`
  color: ${({ fColor }): string => fColor};
`;

const ComparativeTable = styled.table.attrs({
  className: `
  w-100
  `,
})`
  border-collapse: separate;
  border-spacing: 0 15px;

  tr:first-child th:first-child {
    border-top-left-radius: 5px;
  }
  tr:first-child th:last-child {
    border-top-right-radius: 5px;
  }
  tr:last-child th:first-child {
    border-bottom-left-radius: 5px;
  }
  tr:last-child th:last-child {
    border-bottom-right-radius: 5px;
  }

  tr:first-child td:first-child {
    border-top-left-radius: 5px;
  }
  tr:first-child td:last-child {
    border-top-right-radius: 5px;
  }
  tr:last-child td:first-child {
    border-bottom-left-radius: 5px;
  }
  tr:last-child td:last-child {
    border-bottom-right-radius: 5px;
  }

  @media (max-width: 800px) {
    min-width: 725px;
  }
`;

const TableRow = styled.tr`
  box-shadow: 0px 2px 5px 0px rgba(0, 0, 0, 0.15);
`;

const HeadCol = styled.th.attrs({
  className: `
    pv2
  `,
})`
  background-color: #5c5c70;
`;

const TableCol = styled.td.attrs({
  className: `
    tl
    pv4
    ph4
    v-top
  `,
})`
  background-color: #ffffff;
`;

export {
  BoldColor,
  ComparativeTable,
  Container,
  HeadCol,
  TableCol,
  TableContainer,
  TableDescription,
  TableRow,
};
