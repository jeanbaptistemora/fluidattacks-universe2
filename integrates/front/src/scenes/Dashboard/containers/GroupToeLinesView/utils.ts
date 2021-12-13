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

const onSelectSeveralToeLinesHelper = (
  isSelect: boolean,
  toeLinesDatasSelected: IToeLinesData[],
  selectedToeLinesDatas: IToeLinesData[],
  setSelectedToeLines: (value: React.SetStateAction<IToeLinesData[]>) => void
): string[] => {
  if (isSelect) {
    const toeLinesToSet: IToeLinesData[] = Array.from(
      new Set([...selectedToeLinesDatas, ...toeLinesDatasSelected])
    );
    setSelectedToeLines(toeLinesToSet);

    return toeLinesToSet.map((toeLinesData: IToeLinesData): string =>
      getToeLinesId(toeLinesData)
    );
  }
  const toeLinesIds: string[] = getToeLinesIds(toeLinesDatasSelected);
  setSelectedToeLines(
    Array.from(
      new Set(
        selectedToeLinesDatas.filter(
          (selectedToeLinesData: IToeLinesData): boolean =>
            !toeLinesIds.includes(getToeLinesId(selectedToeLinesData))
        )
      )
    )
  );

  return selectedToeLinesDatas.map((toeLinesData: IToeLinesData): string =>
    getToeLinesId(toeLinesData)
  );
};

export { getToeLinesIndex, onSelectSeveralToeLinesHelper };
