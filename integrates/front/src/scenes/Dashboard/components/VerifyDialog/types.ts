/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IVerifyStakeholderResultAttr {
  verifyStakeholder: {
    success: boolean;
  };
}

interface IPhoneAttr {
  callingCountryCode: string;
  countryCode: string;
  nationalNumber: string;
}

interface IGetStakeholderPhoneAttr {
  me: {
    phone: IPhoneAttr | null;
  };
}

interface IVerifyFn {
  (
    verifyCallback: (verificationCode: string) => void,
    cancelCallback: () => void
  ): void;
}

interface IVerifyFormValues {
  verificationCode: string;
}

interface IVerifyDialogProps {
  isOpen: boolean;
  message?: React.ReactNode;
  children: (verify: IVerifyFn) => React.ReactNode;
}

export type {
  IPhoneAttr,
  IGetStakeholderPhoneAttr,
  IVerifyDialogProps,
  IVerifyFormValues,
  IVerifyFn,
  IVerifyStakeholderResultAttr,
};
