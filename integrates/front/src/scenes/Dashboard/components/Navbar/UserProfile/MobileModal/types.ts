import type { IPhoneData } from "utils/forms/fields/PhoneNumber/FormikPhone/types";

interface IUpdateStakeholderPhoneAttr {
  updateStakeholderPhone: {
    success: boolean;
  };
}

interface IPhoneAttr {
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

interface IVerificationFormValues {
  phone: IPhoneData;
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

export {
  IAdditionFormValues,
  IPhoneAttr,
  IHandleAdditionModalFormProps,
  IPhoneNumberFieldProps,
  IUpdateStakeholderPhoneAttr,
  IGetStakeholderPhoneAttr,
  IMobileModalProps,
  IVerificationFormValues,
};
