interface IFormData {
  comments: string;
  confirmation: string;
  drills: boolean;
  forces: boolean;
  integrates: boolean;
  organization: string;
  reason: string;
  type: string;
}

interface IGroupData {
  project: {
    hasDrills: boolean;
    hasForces: boolean;
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
