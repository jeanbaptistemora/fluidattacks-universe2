export interface IProjectData {
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

export interface IProjectRoute {
  setUserRole(userRole: string | undefined): void;
}
