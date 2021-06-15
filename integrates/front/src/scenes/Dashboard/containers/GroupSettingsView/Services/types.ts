interface IFormData {
  comments: string;
  confirmation: string;
  squad: boolean;
  forces: boolean;
  integrates: boolean;
  organization: string;
  reason: string;
  machine: boolean;
  type: string;
}

interface IGroupData {
  group: {
    hasDrills: boolean;
    hasForces: boolean;
    hasSkims: boolean;
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
