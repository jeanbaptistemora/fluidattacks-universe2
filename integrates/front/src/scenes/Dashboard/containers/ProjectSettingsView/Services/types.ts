export interface IFormData {
  comments: string;
  confirmation: string;
  drills: boolean;
  forces: boolean;
  integrates: boolean;
  organization: string;
  reason: string;
  type: string;
}

export interface IGroupData {
  project: {
    hasDrills: boolean;
    hasForces: boolean;
    organization: {
      name: string;
    };
    subscription: string;
  };
}

export interface IServicesProps {
  groupName: string;
}

export interface IServicesDataSet {
  canHave: boolean;
  onChange?: ((checked: boolean) => void);
  service: string;
}
