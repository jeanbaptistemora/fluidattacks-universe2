export interface IFormData {
  drills: boolean;
  forces: boolean;
  integrates: boolean;
  type: string;
}

export interface IGroupData {
  project: {
    hasDrills: boolean;
    hasForces: boolean;
    subscription: string;
  };
}

export interface IServicesProps {
  groupName: string;
}

export interface IServicesDataSet {
  canHave: boolean;
  disabled: boolean;
  onChange?: ((checked: boolean) => void);
  service: string;
}
