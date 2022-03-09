import _ from "lodash";

import type { IFilterSet, IToeInputData } from "./types";

import {
  filterDateRange,
  filterSearchText,
  filterSelect,
} from "components/Table/utils/filters";

const getToeInputId: (toeInputData: IToeInputData) => string = (
  toeInputData: IToeInputData
): string =>
  toeInputData.rootId + toeInputData.component + toeInputData.entryPoint;

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

const filterHasVulnerabilities: (
  filterGroupToeInputTable: IFilterSet,
  toeInputs: IToeInputData[]
) => IToeInputData[] = (
  filterGroupToeInputTable: IFilterSet,
  toeInputs: IToeInputData[]
): IToeInputData[] => {
  const hasVulnerabilities =
    filterGroupToeInputTable.hasVulnerabilities === "true";

  return _.isEmpty(filterGroupToeInputTable.hasVulnerabilities)
    ? toeInputs
    : toeInputs.filter((toeInputData): boolean => {
        return toeInputData.hasVulnerabilities === hasVulnerabilities;
      });
};

const filterSearchtextResult: (
  searchTextFilter: string,
  toeInputs: IToeInputData[]
) => IToeInputData[] = (
  searchTextFilter: string,
  toeInputs: IToeInputData[]
): IToeInputData[] => filterSearchText(toeInputs, searchTextFilter);

const getFilteredData: (
  filterGroupToeInputTable: IFilterSet,
  searchTextFilter: string,
  toeInput: IToeInputData[]
) => IToeInputData[] = (
  filterGroupToeInputTable: IFilterSet,
  searchTextFilter: string,
  toeInput: IToeInputData[]
): IToeInputData[] => {
  const filteredComponent: IToeInputData[] = filterSelect(
    toeInput,
    filterGroupToeInputTable.component,
    "component"
  );
  const filteredHasVulnerabilities = filterHasVulnerabilities(
    filterGroupToeInputTable,
    toeInput
  );
  const filteredSearchtextResult = filterSearchtextResult(
    searchTextFilter,
    toeInput
  );
  const filteredSeenAt: IToeInputData[] = filterDateRange(
    toeInput,
    filterGroupToeInputTable.seenAt,
    "seenAt"
  );
  const filteredSeenFirstTimeBy: IToeInputData[] = filterSelect(
    toeInput,
    filterGroupToeInputTable.seenFirstTimeBy,
    "markedSeenFirstTimeBy"
  );
  const filteredData: IToeInputData[] = _.intersection(
    filteredComponent,
    filteredHasVulnerabilities,
    filteredSearchtextResult,
    filteredSeenAt,
    filteredSeenFirstTimeBy
  );

  return filteredData;
};

const formatBePresent = (bePresent: string): boolean | undefined =>
  bePresent === "" ? undefined : bePresent === "true";

const formatRootId = (rootId: string): string | undefined =>
  rootId === "" ? undefined : rootId;

export {
  getFilteredData,
  getToeInputIndex,
  onSelectSeveralToeInputHelper,
  formatBePresent,
  formatRootId,
};
