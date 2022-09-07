/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { IAvailableParameter, IParameter } from "./types";

const excludeUniqueParameters = (
  availableParameters: IAvailableParameter[],
  parameters: IParameter[]
): IAvailableParameter[] => {
  const currentParameterNames = parameters.map(
    (parameter): string => parameter.name
  );

  return availableParameters.filter((parameter): boolean => {
    if (parameter.unique) {
      return !currentParameterNames.includes(parameter.name);
    }

    return true;
  });
};

export { excludeUniqueParameters };
