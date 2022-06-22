import styled from "styled-components";

interface IButtonsProps {
  selection: number;
}

const Buttons = styled.div<IButtonsProps>`
  border-radius: 4px;
  display: inline-flex;
  overflow: hidden;

  > button {
    background-color: #e9e9ed;
    border: 1px solid #d2d2da;
    color: #2e2e38;
    font-size: 16px;
    padding: 10px 16px;
    transition: all 0.3s ease;

    :hover {
      background-color: #c7c7d1;
    }
  }

  button:not(:first-child) {
    border-left-style: none;
  }

  button:nth-child(${({ selection }): number => selection + 1}) {
    background-color: #2e2e38;
    border-color: #121216;
    color: #e9e9ed;

    :hover {
      background-color: #49495a;
      border-color: #2e2e38;
    }
  }
`;

export type { IButtonsProps };
export { Buttons };
