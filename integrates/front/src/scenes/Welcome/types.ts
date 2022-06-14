interface IGetUserWelcomeResult {
  me: {
    organizations: {
      groups: {
        name: string;
        roots: {
          url: string;
        }[];
      }[];
      name: string;
    }[];
    remember: boolean;
    userEmail: string;
    userName: string;
  };
}

export type { IGetUserWelcomeResult };
