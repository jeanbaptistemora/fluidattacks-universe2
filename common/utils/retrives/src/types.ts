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

export { Group, Organization, GitRoot };
