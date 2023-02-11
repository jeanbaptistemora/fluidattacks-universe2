interface ITrial {
  completed: boolean;
}

interface IGroups {
  managed: "MANAGED" | "NOT_MANAGED" | "TRIAL" | "UNDER_REVIEW";
  name: string;
}

interface IOrgs {
  groups: IGroups[];
  name: string;
}

interface IGetStakeholderEnrollmentResult {
  me: {
    enrolled: boolean;
    organizations: IOrgs[];
    trial: ITrial | null;
    userEmail: string;
    userName: string;
  };
}

export type { IGetStakeholderEnrollmentResult };
