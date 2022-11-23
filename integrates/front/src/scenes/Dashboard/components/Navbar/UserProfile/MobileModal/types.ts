import type { IPhoneData } from "utils/forms/fields/PhoneNumber/FormikPhone/types";

interface IUpdateStakeholderPhoneResultAttr {
  updateStakeholderPhone: {
    success: boolean;
  };
}

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

interface IAdditionFormValues {
  phone: IPhoneData;
}

interface IVerifyAdditionCodeFormValues {
  phone: IPhoneData;
  newVerificationCode: string;
}

interface IEditionFormValues {
  phone: IPhoneData;
  newPhone: IPhoneData;
  verificationCode: string;
}

interface IVerifyEditionFormValues {
  phone: IPhoneData;
  newPhone: IPhoneData;
  newVerificationCode: string;
  verificationCode: string;
}

interface IHandleAdditionModalFormProps {
  handleCloseModal: () => void;
}

interface IPhoneNumberFieldProps {
  disable: boolean;
}

interface IMobileModalProps {
  onClose: () => void;
}

export type {
  IAdditionFormValues,
  IPhoneAttr,
  IHandleAdditionModalFormProps,
  IPhoneNumberFieldProps,
  IUpdateStakeholderPhoneResultAttr,
  IGetStakeholderPhoneAttr,
  IMobileModalProps,
  IVerifyAdditionCodeFormValues,
  IVerifyStakeholderResultAttr,
  IEditionFormValues,
  IVerifyEditionFormValues,
};
