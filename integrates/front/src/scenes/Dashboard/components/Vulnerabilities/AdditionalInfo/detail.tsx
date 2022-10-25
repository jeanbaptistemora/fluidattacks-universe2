/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";
import React from "react";

import { Label } from "./styles";
import { Value } from "./value";

export const Detail: React.FC<{
  editableField: JSX.Element | undefined;
  isEditing: boolean;
  label: string | undefined;
  value: number | string | undefined;
}> = ({
  isEditing,
  editableField,
  label,
  value,
}: {
  editableField: JSX.Element | undefined;
  isEditing: boolean;
  label: string | undefined;
  value: number | string | undefined;
}): JSX.Element => {
  return (
    <React.StrictMode>
      <div className={"flex flex-row  justify-start items-end"}>
        {_.isUndefined(label) ? undefined : (
          <div>
            <Label>{label}</Label>&nbsp;
          </div>
        )}
        <div>{isEditing ? editableField : <Value value={value} />}</div>
      </div>
    </React.StrictMode>
  );
};
