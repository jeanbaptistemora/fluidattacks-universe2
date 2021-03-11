interface IProjectData {
  alert: {
    message: string;
    status: number;
  };
  project: {
    deletionDate: string;
    organization: string;
    serviceAttributes: string[];
    userDeletion: string;
  };
}

interface IProjectRoute {
  setUserRole: (userRole: string | undefined) => void;
}

export { IProjectData, IProjectRoute };
