import type { IToeLinesData } from "./types";

const getToeLinesId: (toeLinesData: IToeLinesData) => string = (
  toeLinesData: IToeLinesData
): string => toeLinesData.rootId + toeLinesData.filename;

const getToeLinesIds: (toeLines: IToeLinesData[]) => string[] = (
  toeLines: IToeLinesData[]
): string[] =>
  toeLines.map((toeLinesData: IToeLinesData): string =>
    getToeLinesId(toeLinesData)
  );

export { getToeLinesIds };
