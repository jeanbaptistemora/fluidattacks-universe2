interface IGetUserWelcomeResult {
  me: {
    userEmail: string;
    organizations: {
      name: string;
    }[];
  };
}

export type { IGetUserWelcomeResult };
