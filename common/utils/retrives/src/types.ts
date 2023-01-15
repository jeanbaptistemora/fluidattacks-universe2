interface Group {
  name: string;
  subscription: string;
}

interface Organization {
  groups: Group[];
}

interface GitRoot {
  nickname: string;
  downloadUrl?: string;
}

export type { Group, Organization, GitRoot };
