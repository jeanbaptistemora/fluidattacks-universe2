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

export {
  IPhoneAttr,
  IGetStakeholderPhoneAttr,
  IVerifyDialogProps,
  IVerifyFormValues,
  IVerifyFn,
  IVerifyStakeholderResultAttr,
};
