import { ILastLogin } from "../scenes/Dashboard/containers/ProjectStakeholdersView/types";

export const sortLastLogin: (
  a: ILastLogin,
  b: ILastLogin,
  order: "desc" | "asc"
) => number = (a: ILastLogin, b: ILastLogin, order: "desc" | "asc"): number => {
  if (order === "asc") {
    if (a.value[0] === 0 && b.value[0] === 0) {
      return a.value[1] - b.value[1];
    }

    return a.value[0] - b.value[0];
  }
  if (a.value[0] === 0 && b.value[0] === 0) {
    return b.value[1] - a.value[1];
  }

  return b.value[0] - a.value[0];
};
