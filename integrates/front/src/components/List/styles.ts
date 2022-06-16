import styled from "styled-components";

interface IContainerProps {
  columns: number;
}

const Container = styled.div<IContainerProps>`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  > * {
    width: ${({ columns }): number => 100 / columns}%;
  }
`;

const Item = styled.div`
  align-items: center;
  display: flex;
  justify-content: center;
`;

export type { IContainerProps };
export { Container, Item };
