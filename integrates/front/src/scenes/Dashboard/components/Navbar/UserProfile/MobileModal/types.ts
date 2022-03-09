interface IUpdateStakeholderPhoneAttr {
  updateStakeholderPhone: {
    success: boolean;
  };
}

interface IPhone {
  countryDialCode: string;
  countryIso2: string;
  localNumber: string;
}

interface IGetStakeholderPhoneAttr {
  me: {
    phone: IPhone | null;
  };
}

interface IAdditionFormValues {
  phone: IPhone;
}

interface IVerificationFormValues {
  phone: IPhone;
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
  IPhone,
  IHandleAdditionModalFormProps,
  IPhoneNumberFieldProps,
  IUpdateStakeholderPhoneAttr,
  IGetStakeholderPhoneAttr,
  IMobileModalProps,
  IVerificationFormValues,
};
