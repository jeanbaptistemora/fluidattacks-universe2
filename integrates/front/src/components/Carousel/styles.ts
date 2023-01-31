import styled from "styled-components";

interface IButtonsProps {
  selection: number;
}

const Buttons = styled.div<IButtonsProps>`
  height: 264;
  display: inline-flex;
  overflow: hidden;

  > button {
    border-radius: 100%;
    border-color: #fff;
    color: #fff;
    margin-right: 8px;
    margin-top: 24px;
    margin-bottom: 24px;
  }

  button:nth-child(${({ selection }): number => selection + 1}) {
    background-color: #65657b;
    color: #fff;
  }
`;

export type { IButtonsProps };
export { Buttons };
