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
    userName: string;
  };
}

interface IGetStakeholderEnrollmentResult {
  me: {
    enrollment: IEnrollment;
  };
}

export type {
  IGetStakeholderEnrollmentResult,
  IGetStakeholderWelcomeResult,
  IEnrollment,
};
