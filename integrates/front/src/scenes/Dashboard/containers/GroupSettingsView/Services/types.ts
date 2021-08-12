interface IFormData {
  asm: boolean;
  comments: string;
  confirmation: string;
  forces?: boolean;
  machine: boolean;
  reason: string;
  organization?: string;
  service: string;
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
    service: string;
    subscription: string;
  };
}

interface IServicesProps {
  groupName: string;
}

interface IServicesFormProps {
  data: IGroupData | undefined;
  groupName: string;
  isModalOpen: boolean;
  loadingGroupData: boolean;
  setIsModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  submittingGroupData: boolean;
}

interface IServicesDataSet {
  id: string;
  onChange?: (checked: boolean) => void;
  service: string;
}

export {
  IFormData,
  IGroupData,
  IServicesDataSet,
  IServicesFormProps,
  IServicesProps,
};
