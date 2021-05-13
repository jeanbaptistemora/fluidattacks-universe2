import _ from "lodash";

import type { IOrganization, IOrgsResult } from "./types";

const hasAnalytics = (organization: IOrganization): boolean =>
  !_.isNil(organization.analytics);

const getOrgs = (
  data: IOrgsResult | undefined,
  emptyOrg: IOrganization
): IOrganization[] =>
  data === undefined || data.me.organizations.filter(hasAnalytics).length === 0
    ? [emptyOrg]
    : _.sortBy(data.me.organizations.filter(hasAnalytics), "name");

export { getOrgs };
