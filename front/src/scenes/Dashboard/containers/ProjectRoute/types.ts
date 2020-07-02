export interface IProjectData {
  alert: {
    message: string;
    status: number;
  };
  project: {
    deletionDate: string;
    serviceAttributes: string[];
    userDeletion: string;
  };
}

export interface IProjectRoute {
  setUserRole(userRole: string | undefined): void;
}

export interface IRejectRemoveProject {
  rejectRemoveProject: {
    success: boolean;
  };
}
