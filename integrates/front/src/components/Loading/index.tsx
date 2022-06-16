import styled, { keyframes } from "styled-components";

interface ILoadingProps {
  size: number;
}

const spinAnim = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const Loading = styled.div<ILoadingProps>`
  animation: ${spinAnim} 1s linear infinite;
  border: ${({ size }): number => size / 7 + 1}px solid #dddde3;
  border-top: ${({ size }): number => size / 7 + 1}px solid #a5a5b6;
  border-radius: 50%;
  display: inline-block;
  height: ${({ size }): number => size}px;
  width: ${({ size }): number => size}px;
`;

export type { ILoadingProps };
export { Loading };
