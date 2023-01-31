import styled from "styled-components";

interface IProgressBarProps {
  max: number;
  value: number;
}

const Container = styled.div`
  height: 20px;
  padding: 6px;
  position: relative;
  width: 100%;
`;

const ProgressBar = styled.div<IProgressBarProps>`
  background-color: #d2d2da;
  border-radius: 4px;
  height: 100%;
  position: relative;
  width: 100%;

  ::before {
    content: " ";
    background-color: #8f8fa3;
    border-radius: 4px;
    height: 100%;
    position: absolute;
    top: 0;
    transition: width 0.3s linear;
    width: ${({ max, value }): number => (value / max) * 100}%;
  }
`;

const StepsContainer = styled.div`
  color: #65657b;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;

  left: 0;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);

  > * {
    background-color: #d2d2da;
    border-radius: 50%;
    padding: 2px;
  }
`;

export type { IProgressBarProps };
export { Container, ProgressBar, StepsContainer };
