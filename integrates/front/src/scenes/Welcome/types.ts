interface IEnrollment {
  enrolled: boolean;
}

interface IGetStakeholderEnrollmentResult {
  me: {
    enrollment: IEnrollment;
    userEmail: string;
    userName: string;
  };
}

export type { IGetStakeholderEnrollmentResult, IEnrollment };
