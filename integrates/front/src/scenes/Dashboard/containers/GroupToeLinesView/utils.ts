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

const getToeLinesIndex: (
  selectedToeLinesDatas: IToeLinesData[],
  allToeLinesDatas: IToeLinesData[]
) => number[] = (
  selectedToeLinesDatas: IToeLinesData[],
  allToeLinesDatas: IToeLinesData[]
): number[] => {
  const selectToeLinesIds: string[] = getToeLinesIds(selectedToeLinesDatas);

  return allToeLinesDatas.reduce(
    (
      selectedToeLinesIndex: number[],
      currentToeLinesData: IToeLinesData,
      currentToeLinesDataIndex: number
    ): number[] =>
      selectToeLinesIds.includes(getToeLinesId(currentToeLinesData))
        ? [...selectedToeLinesIndex, currentToeLinesDataIndex]
        : selectedToeLinesIndex,
    []
  );
};

export { getToeLinesIndex };
