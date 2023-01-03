interface Group {
  name: string;
  subscription: string;
}

interface Organization {
  groups: Group[];
}

export { Group, Organization };
