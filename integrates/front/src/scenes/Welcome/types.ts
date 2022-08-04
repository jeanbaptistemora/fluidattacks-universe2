interface IEnrollment {
  enrolled: boolean;
}
interface IGetStakeholderWelcomeResult {
  me: {
    organizations: {
      groups: {
        name: string;
        roots: {
          url: string;
        }[];
        service: string;
        subscription: string;
      }[];
      name: string;
    }[];
    remember: boolean;
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
