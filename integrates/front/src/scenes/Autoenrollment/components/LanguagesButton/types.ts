import type { IPhoneData } from "utils/forms/fields/PhoneNumber/FormikPhone/types";

interface ISendSalesMailToGetSquadPlan {
  sendSalesMailToGetSquadPlan: {
    success: boolean;
  };
}

interface IAdditionFormValues {
  email: string;
  name: string;
  phone: IPhoneData;
}

interface IGetStakeholderResult {
  me: {
    userEmail: string;
    userName: string;
  };
}

export type {
  ISendSalesMailToGetSquadPlan,
  IAdditionFormValues,
  IGetStakeholderResult,
};
