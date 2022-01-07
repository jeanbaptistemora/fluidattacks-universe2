import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faSyncAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, {
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import { Button } from "components/Button";
import { filterSearchText } from "components/DataTableNext/utils";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { formatVulnerabilitiesTreatment } from "scenes/Dashboard/components/Vulnerabilities/utils";
import { AssignedVulnerabilitiesContext } from "scenes/Dashboard/context";
import type {
  IGetUserOrganizationsGroups,
  IGetVulnsGroups,
  IOrganizationGroups,
} from "scenes/Dashboard/types";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";

interface ITasksContent {
  setUserRole: (userRole: string | undefined) => void;
  userData: IGetUserOrganizationsGroups | undefined;
  setTaskState: (taskState: boolean) => void;
  taskState: boolean;
}

interface IAction {
  action: string;
}

export const TasksContent: React.FC<ITasksContent> = ({
  setUserRole,
  userData,
  setTaskState,
  taskState,
}: ITasksContent): JSX.Element => {
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRetrieveHacker: boolean = permissions.can(
    "api_resolvers_vulnerability_hacker_resolve"
  );

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const attributesContext: PureAbility<string> = useContext(authzGroupContext);
  const permissionsContext: PureAbility<string> = useContext(
    authzPermissionsContext
  );
  const userGroupsRoles: string[] = useMemo(
    (): string[] =>
      userData === undefined || _.isEmpty(userData)
        ? []
        : _.flatten(
            userData.me.organizations.map(
              (organization: IOrganizationGroups): string[] =>
                organization.groups.map(
                  (group: IOrganizationGroups["groups"][0]): string =>
                    group.userRole
                )
            )
          ),
    [userData]
  );
  const [allData] = useContext(AssignedVulnerabilitiesContext);

  const onGroupChange: () => void = (): void => {
    attributesContext.update([]);
    permissionsContext.update([]);
    if (userData !== undefined && userGroupsRoles.length > 0) {
      const currentPermissions: IAction[][] = _.flatten(
        userData.me.organizations.map(
          (organization: IOrganizationGroups): IAction[][] =>
            organization.groups.map(
              (group: IOrganizationGroups["groups"][0]): IAction[] =>
                group.permissions.map(
                  (action: string): IAction => ({
                    action,
                  })
                )
            )
        )
      );
      if (currentPermissions.length > 0 && currentPermissions[0].length > 0) {
        permissionsContext.update(
          Array.from(
            new Set(
              currentPermissions.reduce(
                (
                  selectedPermission: IAction[],
                  currentPermission: IAction[]
                ): IAction[] =>
                  currentPermission.length < selectedPermission.length
                    ? currentPermission
                    : selectedPermission,
                currentPermissions[0]
              )
            )
          )
        );
      }
      setUserRole(userGroupsRoles[0]);
    }
  };

  useEffect(onGroupChange, [
    attributesContext,
    permissionsContext,
    setUserRole,
    userData,
    userGroupsRoles,
  ]);

  const [, setRemediationModalConfig] = useState<{
    vulnerabilities: IVulnRowAttr[];
    clearSelected: () => void;
  }>({
    clearSelected: (): void => undefined,
    vulnerabilities: [],
  });

  const openRemediationModal: (
    vulnerabilities: IVulnRowAttr[],
    clearSelected: () => void
  ) => void = useCallback(
    (vulnerabilities: IVulnRowAttr[], clearSelected: () => void): void => {
      setRemediationModalConfig({ clearSelected, vulnerabilities });
    },
    []
  );

  const refreshAssigned: () => void = useCallback((): void => {
    setTaskState(!taskState);
  }, [setTaskState, taskState]);

  if (_.isUndefined(userData) || _.isEmpty(userData)) {
    return <div />;
  }

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchTextVulnerabilities: IVulnRowAttr[] = filterSearchText(
    formatVulnerabilitiesTreatment(
      _.flatten(
        allData.map((group: IGetVulnsGroups): IVulnRowAttr[] =>
          group.group.vulnerabilitiesAssigned.map(
            (vulnerability: IVulnRowAttr): IVulnRowAttr => ({
              ...vulnerability,
              groupName: group.group.name,
            })
          )
        )
      )
    ),
    searchTextFilter
  );

  return (
    <React.StrictMode>
      <VulnComponent
        canDisplayHacker={canRetrieveHacker}
        customSearch={{
          customSearchDefault: searchTextFilter,
          isCustomSearchEnabled: true,
          onUpdateCustomSearch: onSearchTextChange,
          position: "right",
        }}
        extraButtons={
          <Button onClick={refreshAssigned}>
            <FontAwesomeIcon icon={faSyncAlt} />
          </Button>
        }
        findingState={"open"}
        isEditing={false}
        isFindingReleased={true}
        isRequestingReattack={false}
        isVerifyingRequest={false}
        onVulnSelect={openRemediationModal}
        vulnerabilities={filterSearchTextVulnerabilities}
      />
    </React.StrictMode>
  );
};
