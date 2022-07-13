import styled, { keyframes } from "styled-components";

interface ILoadingProps {
  anim?: "ease" | "linear";
  size?: number;
}

const spinAnim = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const Loading = styled.div<ILoadingProps>`
  animation: ${spinAnim} 1s linear infinite;
  ${({ anim = "linear", size = 24 }): string => `
  animation-timing-function: ${anim};
  border: ${Math.ceil(size / 7)}px solid #dddde3;
  border-top: ${Math.ceil(size / 7)}px solid #a5a5b6;
  border-radius: 50%;
  display: inline-block;
  height: ${size}px;
  width: ${size}px;
  `}
`;

export type { ILoadingProps };
export { Loading };
