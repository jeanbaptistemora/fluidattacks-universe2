interface IGroupData {
  alert: {
    message: string;
    status: number;
  };
  group: {
    deletionDate: string;
    organization: string;
    serviceAttributes: string[];
    userDeletion: string;
  };
}

interface IGroupRoute {
  setUserRole: (userRole: string | undefined) => void;
}

export { IGroupData, IGroupRoute };
