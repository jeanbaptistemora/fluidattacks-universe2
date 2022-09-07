/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { LinkSpan } from "./styles";

interface ILinkRowProps {
  onClick: () => void;
  value: string;
}

const LinkRow: React.FC<ILinkRowProps> = ({
  onClick,
  value,
}: Readonly<ILinkRowProps>): JSX.Element => {
  return (
    <React.StrictMode>
      <LinkSpan isNone={value === "None"} onClick={onClick}>
        {value}
      </LinkSpan>
    </React.StrictMode>
  );
};

export type { ILinkRowProps };
export { LinkRow };
