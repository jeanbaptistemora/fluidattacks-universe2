import _ from "lodash";
import React from "react";

import type { ILocationsInfoAttr } from "../types";

export const locationsFormatter: (
  locationsInfo: ILocationsInfoAttr
) => JSX.Element = (locationsInfo: ILocationsInfoAttr): JSX.Element => {
  const { locations, openVulnerabilities, closedVulnerabilities } =
    locationsInfo;
  const firstLocation: string | undefined = _.isUndefined(locations)
    ? undefined
    : _.first(
        locations.split(",", 2).map((element: string): string => element.trim())
      );
  const locationsTotal = openVulnerabilities + closedVulnerabilities;
  const additional = locationsTotal - 1;

  return (
    <div>
      {_.isUndefined(firstLocation) ? undefined : (
        <p className={`mb0 tl truncate`}>
          {firstLocation}&nbsp;
          {additional > 0 ? <b>{`+${additional}`}</b> : undefined}
        </p>
      )}
    </div>
  );
};
