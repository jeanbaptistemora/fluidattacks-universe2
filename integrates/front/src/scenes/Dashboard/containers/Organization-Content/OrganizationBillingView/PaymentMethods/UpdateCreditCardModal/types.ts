interface IUpdateCreditCardModalProps {
  onClose: () => void;
  onSubmit: (values: {
    cardExpirationMonth: number | undefined;
    cardExpirationYear: number | undefined;
    makeDefault: boolean;
  }) => Promise<void>;
}

interface IUpdateOtherMethodsModalProps {
  onClose: () => void;
  onSubmit: (values: {
    businessName: string;
    city: string;
    country: string;
    email: string;
    rutList: FileList | undefined;
    state: string;
    taxIdList: FileList | undefined;
  }) => Promise<void>;
}

export type { IUpdateCreditCardModalProps, IUpdateOtherMethodsModalProps };
