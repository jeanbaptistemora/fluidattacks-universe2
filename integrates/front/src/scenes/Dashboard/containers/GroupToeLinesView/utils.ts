import _ from "lodash";

import type { IFilterSet, IToeLinesData } from "./types";

import {
  filterDateRange,
  filterSearchText,
  filterSelect,
} from "components/Table/utils/filters";

const PERCENTBASE = 100;

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

function getNonSelectable(toeLinesDatas: IToeLinesData[]): number[] {
  const nonSelectable: number[] = toeLinesDatas.reduce(
    (
      nonSelectableToeLinesDatas: number[],
      toeLinesData: IToeLinesData,
      currentToeLinesDataIndex: number
    ): number[] =>
      toeLinesData.bePresent
        ? nonSelectableToeLinesDatas
        : [...nonSelectableToeLinesDatas, currentToeLinesDataIndex],
    []
  );

  return nonSelectable;
}

const filterBooleanValue: (
  filterGroupToeLinesTable: IFilterSet,
  filterName: keyof IFilterSet,
  toeLines: IToeLinesData[],
  columnKey: keyof IToeLinesData
) => IToeLinesData[] = (
  filterGroupToeLinesTable: IFilterSet,
  filterName: keyof IFilterSet,
  toeLines: IToeLinesData[],
  columnKey: keyof IToeLinesData
): IToeLinesData[] => {
  const filterValue = _.isEmpty(filterGroupToeLinesTable[filterName])
    ? undefined
    : filterGroupToeLinesTable[filterName] === "true";

  return _.isUndefined(filterValue)
    ? toeLines
    : toeLines.filter((toeLinesData): boolean => {
        return toeLinesData[columnKey] === filterValue;
      });
};

const filterCoverage: (
  filterGroupToeLinesTable: IFilterSet,
  toeLines: IToeLinesData[]
) => IToeLinesData[] = (
  filterGroupToeLinesTable: IFilterSet,
  toeLines: IToeLinesData[]
): IToeLinesData[] => {
  const coverageMax =
    parseFloat(filterGroupToeLinesTable.coverage.max) / PERCENTBASE;
  const coverageMin =
    parseFloat(filterGroupToeLinesTable.coverage.min) / PERCENTBASE;
  const filteredcoverageMax: IToeLinesData[] = isNaN(coverageMax)
    ? toeLines
    : toeLines.filter((toeLinesData): boolean => {
        return toeLinesData.coverage <= coverageMax;
      });

  return isNaN(coverageMin)
    ? filteredcoverageMax
    : filteredcoverageMax.filter((toeLinesData): boolean => {
        return coverageMin <= toeLinesData.coverage;
      });
};

const filterPriority: (
  filterGroupToeLinesTable: IFilterSet,
  toeLines: IToeLinesData[]
) => IToeLinesData[] = (
  filterGroupToeLinesTable: IFilterSet,
  toeLines: IToeLinesData[]
): IToeLinesData[] => {
  const priorityMax = parseFloat(filterGroupToeLinesTable.priority.max);
  const priorityMin = parseFloat(filterGroupToeLinesTable.priority.min);
  const filteredPriorityMax: IToeLinesData[] = isNaN(priorityMax)
    ? toeLines
    : toeLines.filter((toeLinesData): boolean => {
        return (
          toeLinesData.sortsRiskLevel >= 0 &&
          toeLinesData.sortsRiskLevel <= priorityMax
        );
      });

  return isNaN(priorityMin)
    ? filteredPriorityMax
    : filteredPriorityMax.filter((toeLinesData): boolean => {
        return (
          toeLinesData.sortsRiskLevel >= 0 &&
          priorityMin <= toeLinesData.sortsRiskLevel
        );
      });
};

const filterSearchtextResult: (
  searchTextFilter: string,
  toeLines: IToeLinesData[]
) => IToeLinesData[] = (
  searchTextFilter: string,
  toeLines: IToeLinesData[]
): IToeLinesData[] => filterSearchText(toeLines, searchTextFilter);

const getFilteredData: (
  filterGroupToeLinesTable: IFilterSet,
  searchTextFilter: string,
  toeLines: IToeLinesData[]
) => IToeLinesData[] = (
  filterGroupToeLinesTable: IFilterSet,
  searchTextFilter: string,
  toeLines: IToeLinesData[]
): IToeLinesData[] => {
  const filteredCoverage: IToeLinesData[] = filterCoverage(
    filterGroupToeLinesTable,
    toeLines
  );
  const filteredFilenameExtensions: IToeLinesData[] = filterSelect(
    toeLines,
    filterGroupToeLinesTable.filenameExtension,
    "extension"
  );
  const filteredHasVulnerabilities = filterBooleanValue(
    filterGroupToeLinesTable,
    "hasVulnerabilities",
    toeLines,
    "hasVulnerabilities"
  );
  const filteredModifiedDate: IToeLinesData[] = filterDateRange(
    toeLines,
    filterGroupToeLinesTable.modifiedDate,
    "modifiedDate"
  );
  const filteredPriority = filterPriority(filterGroupToeLinesTable, toeLines);
  const filteredSearchtextResult = filterSearchtextResult(
    searchTextFilter,
    toeLines
  );
  const filteredSeenAt: IToeLinesData[] = filterDateRange(
    toeLines,
    filterGroupToeLinesTable.seenAt,
    "seenAt"
  );
  const filteredData: IToeLinesData[] = _.intersection(
    filteredCoverage,
    filteredFilenameExtensions,
    filteredHasVulnerabilities,
    filteredModifiedDate,
    filteredPriority,
    filteredSearchtextResult,
    filteredSeenAt
  );

  return filteredData;
};

const formatBePresent = (bePresent: string): boolean | undefined =>
  bePresent === "" ? undefined : bePresent === "true";

const formatRootId = (rootId: string): string | undefined =>
  rootId === "" ? undefined : rootId;

export {
  formatBePresent,
  formatRootId,
  getFilteredData,
  getNonSelectable,
  getToeLinesIndex,
  onSelectSeveralToeLinesHelper,
};
