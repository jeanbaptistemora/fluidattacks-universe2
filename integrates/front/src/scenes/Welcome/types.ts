interface IGetUserWelcomeResult {
  me: {
    organizations: {
      name: string;
    }[];
    userEmail: string;
    userName: string;
  };
}

export type { IGetUserWelcomeResult };
