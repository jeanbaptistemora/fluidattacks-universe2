/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";

import type { IStakeholderAttrs } from "scenes/Dashboard/components/AddUserModal/types";

const getUserData = (
  data: IStakeholderAttrs | undefined
): Record<string, string> =>
  _.isEmpty(data) || _.isUndefined(data) ? {} : data.stakeholder;

const getNewInitialValues = (
  initialValues: Record<string, string>,
  action: string,
  organizationModal: boolean
): Record<string, string> =>
  action === "edit"
    ? {
        email: initialValues.email,
        responsibility: organizationModal ? "" : initialValues.responsibility,
        role: initialValues.role.toUpperCase(),
      }
    : {};

export { getUserData, getNewInitialValues };
