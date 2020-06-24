export interface IProjectData {
  project: {
    deletionDate: string;
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
