/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

interface IFloatingProps {
  side: "left" | "right";
}

interface ILabelProps {
  size: number;
}

const Floating = styled.div.attrs({
  className: "comp-toggle",
})<IFloatingProps>`
  ${({ side }): string => `
  height: 72%;
  left: ${side === "left" ? 28 : 72}%;
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  transition: all 0.3s ease;
  width: 36%;
  > * {
    height: 100%;
    width: 100%;
  }
`}
`;

const Input = styled.input`
  display: none;
`;

const Label = styled.label<ILabelProps>`
  ${({ size }): string => `
  background-color: #e9e9ed;
  border: ${Math.ceil(size / 24)}px solid #c7c7d1;
  border-radius: ${size}px;
  color: #65657b;
  display: inline-block;
  height: ${size}px;
  position: relative;
  width: ${size * 2}px;
`}
`;

export type { IFloatingProps, ILabelProps };
export { Floating, Input, Label };
