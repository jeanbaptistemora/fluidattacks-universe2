interface IGroupBill {
  authorsNumber: number;
}

interface IGroupAttr {
  bill: IGroupBill | null;
  forces: string;
  hasForces: boolean;
  hasMachine: boolean;
  hasSquad: boolean;
  machine: string;
  name: string;
  permissions: string[];
  service: string;
  squad: string;
  tier: string;
}

interface IPaymentMethodAttr {
  id: string;
  brand: string;
  default: boolean;
  lastFourDigits: string;
  expirationMonth: string;
  expirationYear: string;
}

export { IGroupAttr, IPaymentMethodAttr };
