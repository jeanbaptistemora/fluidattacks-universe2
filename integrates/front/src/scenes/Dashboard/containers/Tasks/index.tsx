import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faSyncAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useContext, useEffect, useState } from "react";

import { Button } from "components/Button";
import type { IFilterProps } from "components/DataTableNext/types";
import { filterSearchText, filterText } from "components/DataTableNext/utils";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { formatVulnerabilitiesTreatment } from "scenes/Dashboard/components/Vulnerabilities/utils";
import type {
  IAction,
  IFilterTodosSet,
  IGroupAction,
  ITasksContent,
} from "scenes/Dashboard/containers/Tasks/types";
import { AssignedVulnerabilitiesContext } from "scenes/Dashboard/context";
import type {
  IGetVulnsGroups,
  IOrganizationGroups,
} from "scenes/Dashboard/types";
import globalStyle from "styles/global.css";
import { Col100 } from "styles/styledComponents";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";

export const TasksContent: React.FC<ITasksContent> = ({
  userData,
  setTaskState,
  setUserRole,
  taskState,
}: ITasksContent): JSX.Element => {
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRetrieveHacker: boolean = permissions.can(
    "api_resolvers_vulnerability_hacker_resolve"
  );

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("todosLocationsCustomFilters", false);
  const [filterVulnerabilitiesTable, setFilterVulnerabilitiesTable] =
    useStoredState(
      "filterTodosVulnerabilitiesSet",
      {
        tag: "",
      },
      localStorage
    );
  const attributesContext: PureAbility<string> = useContext(authzGroupContext);
  const permissionsContext: PureAbility<string> = useContext(
    authzPermissionsContext
  );
  const [allData] = useContext(AssignedVulnerabilitiesContext);

  const changePermissions = useCallback(
    (groupName: string): void => {
      permissionsContext.update([]);
      if (userData !== undefined) {
        const recordPermissions: IGroupAction[] = _.flatten(
          userData.me.organizations.map(
            (organization: IOrganizationGroups): IGroupAction[] =>
              organization.groups.map(
                (group: IOrganizationGroups["groups"][0]): IGroupAction => ({
                  actions: group.permissions.map(
                    (action: string): IAction => ({
                      action,
                    })
                  ),
                  groupName: group.name,
                })
              )
          )
        );
        const filteredPermissions: IGroupAction[] = recordPermissions.filter(
          (recordPermission: IGroupAction): boolean =>
            recordPermission.groupName.toLowerCase() === groupName.toLowerCase()
        );
        if (filteredPermissions.length > 0) {
          permissionsContext.update(filteredPermissions[0].actions);
        }
      }
    },
    [permissionsContext, userData]
  );

  const onGroupChange: () => void = (): void => {
    attributesContext.update([]);
    permissionsContext.update([]);
    setUserRole(undefined);
    if (userData !== undefined) {
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
    }
  };

  useEffect(onGroupChange, [
    attributesContext,
    permissionsContext,
    userData,
    setUserRole,
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

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }

  const vulnerabilities: IVulnRowAttr[] = formatVulnerabilitiesTreatment(
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
  );

  const onTagChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    event.persist();
    setFilterVulnerabilitiesTable(
      (value): IFilterTodosSet => ({
        ...value,
        tag: event.target.value,
      })
    );
  };

  const filterSearchTextVulnerabilities: IVulnRowAttr[] = filterSearchText(
    vulnerabilities,
    searchTextFilter
  );

  const filterTagVulnerabilities: IVulnRowAttr[] = filterText(
    vulnerabilities,
    filterVulnerabilitiesTable.tag,
    "tag"
  );

  function clearFilters(): void {
    setFilterVulnerabilitiesTable(
      (): IFilterTodosSet => ({
        tag: "",
      })
    );
    setSearchTextFilter("");
  }

  const resultVulnerabilities: IVulnRowAttr[] = _.intersection(
    filterSearchTextVulnerabilities,
    filterTagVulnerabilities
  );

  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: filterVulnerabilitiesTable.tag,
      onChangeInput: onTagChange,
      placeholder: "searchFindings.tabVuln.searchTag",
      tooltipId: "searchFindings.tabVuln.tagTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.tagTooltip",
      type: "text",
    },
  ];
  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  if (_.isUndefined(userData) || _.isEmpty(userData)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <div className={globalStyle.tabContent}>
        <Col100>
          <VulnComponent
            canDisplayHacker={canRetrieveHacker}
            changePermissions={changePermissions}
            clearFiltersButton={clearFilters}
            customFilters={{
              customFiltersProps,
              hideResults: true,
              isCustomFilterEnabled,
              onUpdateEnableCustomFilter: handleUpdateCustomFilter,
              oneRowMessage: true,
              resultSize: {
                current: resultVulnerabilities.length,
                total: vulnerabilities.length,
              },
            }}
            customSearch={{
              customSearchDefault: searchTextFilter,
              isCustomSearchEnabled: true,
              onUpdateCustomSearch: onSearchTextChange,
              position: "right",
            }}
            extraButtons={
              <Button id={"refresh-assigned"} onClick={refreshAssigned}>
                <FontAwesomeIcon icon={faSyncAlt} />
              </Button>
            }
            findingState={"open"}
            hideSelectVulnerability={true}
            isEditing={false}
            isFindingReleased={true}
            isRequestingReattack={false}
            isVerifyingRequest={false}
            onVulnSelect={openRemediationModal}
            vulnerabilities={resultVulnerabilities}
          />
        </Col100>
      </div>
    </React.StrictMode>
  );
};
