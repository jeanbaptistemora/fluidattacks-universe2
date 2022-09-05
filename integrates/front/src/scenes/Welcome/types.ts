interface IEnrollment {
  enrolled: boolean;
}
interface IGetStakeholderWelcomeResult {
  me: {
    organizations: {
      groups: {
        name: string;
      }[];
      name: string;
    }[];
    userEmail: string;
  };
}

interface IGetStakeholderEnrollmentResult {
  me: {
    enrollment: IEnrollment;
    userEmail: string;
    userName: string;
  };
}

export type {
  IGetStakeholderEnrollmentResult,
  IGetStakeholderWelcomeResult,
  IEnrollment,
};
