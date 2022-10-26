/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";
import React from "react";

import { Label } from "./styles";

export const Detail: React.FC<{
  editableField: JSX.Element | undefined;
  isEditing: boolean;
  label: string | undefined;
  field: JSX.Element | string | null;
}> = ({
  isEditing,
  editableField,
  label,
  field,
}: {
  editableField: JSX.Element | undefined;
  isEditing: boolean;
  label: string | undefined;
  field: JSX.Element | string | null;
}): JSX.Element => {
  return (
    <React.StrictMode>
      <div className={" justify-start items-end ma0 pv1"}>
        {_.isUndefined(label) ? undefined : (
          <div style={{ minWidth: "85px" }}>
            <Label>{label}</Label>&nbsp;
          </div>
        )}
        <div>{isEditing ? editableField : field}</div>
      </div>
    </React.StrictMode>
  );
};
