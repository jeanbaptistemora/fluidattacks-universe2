interface IUpdateStakeholderPhoneNumberAttr {
  updateStakeholderPhoneNumber: {
    success: boolean;
  };
}

interface IGetStakeholderPhoneNumberAttr {
  me: {
    phoneNumber: string | null;
  };
}

export { IUpdateStakeholderPhoneNumberAttr, IGetStakeholderPhoneNumberAttr };
