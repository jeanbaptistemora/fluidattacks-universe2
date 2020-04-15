export interface IProjectData {
  project: {
    deletionDate: string;
    userDeletion: string;
  };
}

export interface IRejectRemoveProject {
  rejectRemoveProject: {
    success: boolean;
  };
}
