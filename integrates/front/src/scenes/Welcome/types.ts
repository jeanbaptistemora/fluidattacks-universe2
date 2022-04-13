interface IOnboardingUserData {
  me: {
    userEmail: string;
    organizations: {
      name: string;
    }[];
  };
}

export type { IOnboardingUserData };
