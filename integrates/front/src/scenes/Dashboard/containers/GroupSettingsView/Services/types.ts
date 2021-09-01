interface IFormData {
  asm: boolean;
  comments: string;
  confirmation: string;
  description: string;
  forces?: boolean;
  language: string;
  machine: boolean;
  reason: string;
  organization?: string;
  service: string;
  squad: boolean;
  type: string;
}

interface IGroupData {
  group: {
    description: string;
    hasSquad: boolean;
    hasForces: boolean;
    hasMachine: boolean;
    language: string;
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
