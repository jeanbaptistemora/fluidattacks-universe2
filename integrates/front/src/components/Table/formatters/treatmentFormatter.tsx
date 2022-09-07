/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

export const treatmentFormatter: (value: string) => JSX.Element = (
  value: string
): JSX.Element => {
  const treatmentArray: string[] = value
    .split(",")
    .map((element: string): string => element.trim());

  return (
    <div>
      {treatmentArray.map(
        (treatment: string): JSX.Element => (
          <p key={treatment}>{treatment}</p>
        )
      )}
    </div>
  );
};
