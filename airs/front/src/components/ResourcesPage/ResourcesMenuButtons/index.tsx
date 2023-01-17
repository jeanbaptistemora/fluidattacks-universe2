/* eslint react/forbid-component-props: 0 */
import React, { useCallback, useState } from "react";

import { FilterButton } from "../styledComponents";

interface IProps {
  filterData: (type: string) => void;
}

const ResourcesMenuElements: React.FC<IProps> = ({
  filterData,
}: IProps): JSX.Element => {
  const resourcesFilters = [
    {
      text: "all",
      type: "all-card",
    },
    {
      text: "ebook",
      type: "ebook-card",
    },
    {
      text: "report",
      type: "report-card",
    },
    {
      text: "success story",
      type: "successstory-card",
    },
    {
      text: "webinar",
      type: "webinar-card",
    },
    {
      text: "white paper",
      type: "whitepaper-card",
    },
  ];

  const [selectedFilter, setSelectedFilter] = useState("all-card");

  const onClick = useCallback(
    (type: string): VoidFunction => {
      return (): void => {
        setSelectedFilter(type);
        filterData(type);
      };
    },
    [filterData]
  );

  return (
    <React.Fragment>
      {resourcesFilters.map((resourceFilter): JSX.Element => {
        return (
          <FilterButton
            isSelected={resourceFilter.type === selectedFilter}
            key={resourceFilter.text}
            onClick={onClick(resourceFilter.type)}
          >
            {resourceFilter.text}
          </FilterButton>
        );
      })}
    </React.Fragment>
  );
};

export { ResourcesMenuElements };
