import type { IVulnerability } from "./types";

const formatLocation = (
  _cell: string,
  row: IVulnerability
): React.ReactNode => {
  return `${row.where}:${row.specific}`;
};

export { formatLocation };
