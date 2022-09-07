/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IEnrollment {
  enrolled: boolean;
}
interface IGetStakeholderWelcomeResult {
  me: {
    organizations: {
      groups: {
        name: string;
      }[];
      name: string;
    }[];
    userEmail: string;
  };
}

interface IGetStakeholderEnrollmentResult {
  me: {
    enrollment: IEnrollment;
    userEmail: string;
    userName: string;
  };
}

export type {
  IGetStakeholderEnrollmentResult,
  IGetStakeholderWelcomeResult,
  IEnrollment,
};
