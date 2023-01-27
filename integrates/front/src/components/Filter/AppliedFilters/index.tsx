import _ from "lodash";
import React from "react";

import type { IAppliedFilters } from "./types";
import {
  formatCheckValues,
  formatDateRange,
  formatNumberRange,
  formatValue,
} from "./utils";

import { getMappedOptions } from "../utils";
import { CloseTag } from "components/CloseTag";
import { Container } from "components/Container";
import { Text } from "components/Text";

const AppliedFilters: React.FC<IAppliedFilters> = ({
  filters,
  dataset,
  onClose,
}): JSX.Element => {
  const activeFilters = filters
    .map((filter): JSX.Element | undefined => {
      const { label, rangeValues, type, value, checkValues } = filter;

      const mappedOptions = getMappedOptions(filter, dataset);

      switch (type) {
        case "numberRange": {
          const formattedValue = formatNumberRange(rangeValues);

          return _.isUndefined(formattedValue) ? undefined : (
            <Container key={label} pr={"4px"}>
              <CloseTag
                onClose={onClose(filter)}
                text={`${label} = ${formattedValue}`}
              />
            </Container>
          );
        }
        case "dateRange": {
          const formattedValue = formatDateRange(rangeValues);

          return _.isUndefined(formattedValue) ? undefined : (
            <Container key={label} pr={"4px"}>
              <CloseTag
                onClose={onClose(filter)}
                text={`${label} = ${formattedValue}`}
              />
            </Container>
          );
        }

        case "checkBoxes": {
          const formattedCheckValues = formatCheckValues(
            checkValues,
            mappedOptions
          );

          return _.isUndefined(formattedCheckValues) ? undefined : (
            <Container key={label} pr={"4px"}>
              <CloseTag
                onClose={onClose(filter)}
                text={`${label} = ${formattedCheckValues}`}
              />
            </Container>
          );
        }

        default: {
          const formattedValue = formatValue(value, mappedOptions);

          return _.isUndefined(formattedValue) ? undefined : (
            <Container key={label} pr={"4px"}>
              <CloseTag
                onClose={onClose(filter)}
                text={`${label} = ${formattedValue}`}
              />
            </Container>
          );
        }
      }
    })
    .filter((filter): boolean => {
      return filter !== undefined;
    });

  return (
    <React.Fragment>
      {activeFilters.length > 0 ? (
        <Container pr={"4px"}>
          <Text disp={"inline-block"} fw={7} size={"small"}>
            {"| Filters applied:"}
          </Text>
        </Container>
      ) : null}
      {activeFilters}
    </React.Fragment>
  );
};

export { AppliedFilters };
