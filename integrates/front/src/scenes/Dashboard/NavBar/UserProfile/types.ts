import type { IPhoneData } from "utils/forms/fields/PhoneNumber/FormikPhone/types";

interface IAdditionFormValues {
  phone: IPhoneData;
}

interface IEditionFormValues {
  phone: IPhoneData;
  newPhone: IPhoneData;
  verificationCode: string;
}

interface IGetUserPhoneAttr {
  me: {
    phone: IPhoneAttr | null;
  };
}

interface IPhoneAttr {
  callingCountryCode: string;
  countryCode: string;
  nationalNumber: string;
}

interface IRemoveUserAttr {
  removeStakeholder: {
    success: boolean;
  };
}

interface IUpdateUserPhoneResultAttr {
  updateStakeholderPhone: {
    success: boolean;
  };
}

interface IUserAttrs {
  stakeholder: {
    organization: string;
    responsibility: string;
  };
}

interface IVerifyAdditionCodeFormValues {
  phone: IPhoneData;
  newVerificationCode: string;
}

interface IVerifyEditionFormValues {
  phone: IPhoneData;
  newPhone: IPhoneData;
  newVerificationCode: string;
  verificationCode: string;
}

interface IVerifyUserResultAttr {
  verifyStakeholder: {
    success: boolean;
  };
}

export type {
  IAdditionFormValues,
  IEditionFormValues,
  IGetUserPhoneAttr,
  IPhoneAttr,
  IRemoveUserAttr,
  IUpdateUserPhoneResultAttr,
  IUserAttrs,
  IVerifyAdditionCodeFormValues,
  IVerifyEditionFormValues,
  IVerifyUserResultAttr,
};
