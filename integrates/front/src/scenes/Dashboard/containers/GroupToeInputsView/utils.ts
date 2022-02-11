import type { IToeInputData } from "./types";

const getToeInputId: (toeInputData: IToeInputData) => string = (
  toeInputData: IToeInputData
): string =>
  toeInputData.unreliableRootNickname +
  toeInputData.component +
  toeInputData.entryPoint;

const getToeInputIds: (toeInputs: IToeInputData[]) => string[] = (
  toeInputs: IToeInputData[]
): string[] =>
  toeInputs.map((toeInputData: IToeInputData): string =>
    getToeInputId(toeInputData)
  );

const getToeInputIndex: (
  selectedToeInputDatas: IToeInputData[],
  allToeInputDatas: IToeInputData[]
) => number[] = (
  selectedToeInputDatas: IToeInputData[],
  allToeInputDatas: IToeInputData[]
): number[] => {
  const selectToeInputIds: string[] = getToeInputIds(selectedToeInputDatas);

  return allToeInputDatas.reduce(
    (
      selectedToeInputIndex: number[],
      currentToeInputData: IToeInputData,
      currentToeInputDataIndex: number
    ): number[] =>
      selectToeInputIds.includes(getToeInputId(currentToeInputData))
        ? [...selectedToeInputIndex, currentToeInputDataIndex]
        : selectedToeInputIndex,
    []
  );
};

const onSelectSeveralToeInputHelper = (
  isSelect: boolean,
  toeInputDatasSelected: IToeInputData[],
  selectedToeInputDatas: IToeInputData[],
  setSelectedToeInput: (value: React.SetStateAction<IToeInputData[]>) => void
): string[] => {
  if (isSelect) {
    const toeInputsToSet: IToeInputData[] = Array.from(
      new Set([...selectedToeInputDatas, ...toeInputDatasSelected])
    );
    setSelectedToeInput(toeInputsToSet);

    return toeInputsToSet.map((toeInputData: IToeInputData): string =>
      getToeInputId(toeInputData)
    );
  }
  const toeInputIds: string[] = getToeInputIds(toeInputDatasSelected);
  setSelectedToeInput(
    Array.from(
      new Set(
        selectedToeInputDatas.filter(
          (selectedToeInputData: IToeInputData): boolean =>
            !toeInputIds.includes(getToeInputId(selectedToeInputData))
        )
      )
    )
  );

  return selectedToeInputDatas.map((toeInputData: IToeInputData): string =>
    getToeInputId(toeInputData)
  );
};

export { getToeInputIndex, onSelectSeveralToeInputHelper };
