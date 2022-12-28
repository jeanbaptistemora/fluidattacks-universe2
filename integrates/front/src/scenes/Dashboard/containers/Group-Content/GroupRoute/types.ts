interface IGroupData {
  group: {
    organization: string;
    serviceAttributes: string[];
  };
}

interface IGroupRoute {
  setUserRole: (userRole: string | undefined) => void;
}

export type { IGroupData, IGroupRoute };
