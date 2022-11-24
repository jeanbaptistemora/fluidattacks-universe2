import _ from "lodash";

import { filterDateRange, filterSearchText, filterSelect } from "./filters";
import type { IFilterSet, IIPRootAttr, IToePortData } from "./types";

const getNonSelectableToePortIndex: (
  allToePortDatas: IToePortData[]
) => number[] = (allToePortDatas: IToePortData[]): number[] => {
  return allToePortDatas.reduce(
    (
      selectedToePortIndex: number[],
      currentToePortData: IToePortData,
      currentToePortDataIndex: number
    ): number[] =>
      currentToePortData.bePresent
        ? selectedToePortIndex
        : [...selectedToePortIndex, currentToePortDataIndex],
    []
  );
};

const getToePortId: (toePortData: IToePortData) => string = (
  toePortData: IToePortData
): string =>
  toePortData.rootId + toePortData.address + toePortData.port.toString();

const getToePortIds: (toePorts: IToePortData[]) => string[] = (
  toePorts: IToePortData[]
): string[] =>
  toePorts.map((toePortData: IToePortData): string =>
    getToePortId(toePortData)
  );

const getToePortIndex: (
  selectedToePortDatas: IToePortData[],
  allToePortDatas: IToePortData[]
) => number[] = (
  selectedToePortDatas: IToePortData[],
  allToePortDatas: IToePortData[]
): number[] => {
  const selectToePortIds: string[] = getToePortIds(selectedToePortDatas);

  return allToePortDatas.reduce(
    (
      selectedToePortIndex: number[],
      currentToePortData: IToePortData,
      currentToePortDataIndex: number
    ): number[] =>
      selectToePortIds.includes(getToePortId(currentToePortData))
        ? [...selectedToePortIndex, currentToePortDataIndex]
        : selectedToePortIndex,
    []
  );
};

const onSelectSeveralToePortHelper = (
  isSelect: boolean,
  toePortDatasSelected: IToePortData[],
  selectedToePortDatas: IToePortData[],
  setSelectedToePort: (value: React.SetStateAction<IToePortData[]>) => void
): string[] => {
  if (isSelect) {
    const toePortsToSet: IToePortData[] = Array.from(
      new Set([...selectedToePortDatas, ...toePortDatasSelected])
    );
    setSelectedToePort(toePortsToSet);

    return toePortsToSet.map((toePortData: IToePortData): string =>
      getToePortId(toePortData)
    );
  }
  const toePortIds: string[] = getToePortIds(toePortDatasSelected);
  setSelectedToePort(
    Array.from(
      new Set(
        selectedToePortDatas.filter(
          (selectedToePortData: IToePortData): boolean =>
            !toePortIds.includes(getToePortId(selectedToePortData))
        )
      )
    )
  );

  return selectedToePortDatas.map((toePortData: IToePortData): string =>
    getToePortId(toePortData)
  );
};

const filterHasVulnerabilities: (
  filterGroupToePortTable: IFilterSet,
  toePorts: IToePortData[]
) => IToePortData[] = (
  filterGroupToePortTable: IFilterSet,
  toePorts: IToePortData[]
): IToePortData[] => {
  const hasVulnerabilities =
    filterGroupToePortTable.hasVulnerabilities === "true";

  return _.isEmpty(filterGroupToePortTable.hasVulnerabilities)
    ? toePorts
    : toePorts.filter((toePortData): boolean => {
        return toePortData.hasVulnerabilities === hasVulnerabilities;
      });
};

const filterSearchtextResult: (
  searchTextFilter: string,
  toePorts: IToePortData[]
) => IToePortData[] = (
  searchTextFilter: string,
  toePorts: IToePortData[]
): IToePortData[] => filterSearchText(toePorts, searchTextFilter);

const getFilteredData: (
  filterGroupToePortTable: IFilterSet,
  searchTextFilter: string,
  toePort: IToePortData[]
) => IToePortData[] = (
  filterGroupToePortTable: IFilterSet,
  searchTextFilter: string,
  toePort: IToePortData[]
): IToePortData[] => {
  const filteredComponent: IToePortData[] = filterSelect(
    toePort,
    filterGroupToePortTable.address,
    "address"
  );
  const filteredHasVulnerabilities = filterHasVulnerabilities(
    filterGroupToePortTable,
    toePort
  );
  const filteredSearchtextResult = filterSearchtextResult(
    searchTextFilter,
    toePort
  );
  const filteredSeenAt: IToePortData[] = filterDateRange(
    toePort,
    filterGroupToePortTable.seenAt,
    "seenAt"
  );
  const filteredSeenFirstTimeBy: IToePortData[] = filterSelect(
    toePort,
    filterGroupToePortTable.seenFirstTimeBy,
    "markedSeenFirstTimeBy"
  );
  const filteredData: IToePortData[] = _.intersection(
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

const isEqualRootId = (root: IIPRootAttr | null, rootId: string): boolean => {
  if (_.isNil(root)) {
    return rootId === "";
  }

  return root.id === rootId;
};

export {
  getFilteredData,
  getNonSelectableToePortIndex,
  getToePortIndex,
  onSelectSeveralToePortHelper,
  formatBePresent,
  formatRootId,
  isEqualRootId,
};
