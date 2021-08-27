import _ from "lodash";

import type { IFindingAttr } from "./types";

function filterCurrentStatus(
  findings: IFindingAttr[],
  currentState: string
): IFindingAttr[] {
  return findings.filter((finding: IFindingAttr): boolean =>
    _.isEmpty(currentState) ? true : finding.state === currentState
  );
}

function filterReattack(
  findings: IFindingAttr[],
  currentReattack: string
): IFindingAttr[] {
  return findings.filter((finding: IFindingAttr): boolean =>
    _.isEmpty(currentReattack) ? true : finding.remediated === currentReattack
  );
}

function filterText(
  findings: IFindingAttr[],
  searchText: string
): IFindingAttr[] {
  return findings.filter((finding: IFindingAttr): boolean =>
    _.isEmpty(searchText)
      ? true
      : _.some(finding, (value: unknown): boolean =>
          _.isString(value)
            ? _.includes(value.toLowerCase(), searchText.toLowerCase())
            : false
        )
  );
}

function filterWhere(
  findings: IFindingAttr[],
  searchText: string
): IFindingAttr[] {
  return findings.filter((finding: IFindingAttr): boolean =>
    _.isEmpty(searchText)
      ? true
      : _.includes(finding.where?.toLowerCase(), searchText.toLowerCase())
  );
}

export { filterCurrentStatus, filterReattack, filterText, filterWhere };
