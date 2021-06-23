interface IFormData {
  asm: boolean;
  comments: string;
  confirmation: string;
  forces: boolean;
  machine: boolean;
  reason: string;
  organization: string;
  squad: boolean;
  type: string;
}

interface IGroupData {
  group: {
    hasSquad: boolean;
    hasForces: boolean;
    hasMachine: boolean;
    organization: {
      name: string;
    };
    subscription: string;
  };
}

interface IServicesProps {
  groupName: string;
}

interface IServicesDataSet {
  canHave: boolean;
  id: string;
  onChange?: (checked: boolean) => void;
  service: string;
}

export { IFormData, IGroupData, IServicesDataSet, IServicesProps };
