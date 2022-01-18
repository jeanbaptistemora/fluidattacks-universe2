import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faSyncAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useContext, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import type { IFilterProps } from "components/DataTableNext/types";
import {
  filterSearchText,
  filterSelect,
  filterText,
} from "components/DataTableNext/utils";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  filterTreatment,
  filterTreatmentCurrentStatus,
  formatVulnerabilitiesTreatment,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
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
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRetrieveHacker: boolean = permissions.can(
    "api_resolvers_vulnerability_hacker_resolve"
  );

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [searchGroupName, setSearchGroupName] = useState("");
  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("todosLocationsCustomFilters", false);
  const [filterVulnerabilitiesTable, setFilterVulnerabilitiesTable] =
    useStoredState(
      "filterTodosVulnerabilitiesSet",
      {
        tag: "",
        treatment: "",
        treatmentCurrentStatus: "",
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

  const onTreatmentChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ): void => {
    event.persist();
    setFilterVulnerabilitiesTable(
      (value): IFilterTodosSet => ({
        ...value,
        treatment: event.target.value,
      })
    );
  };

  const onSearchGroupNameChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ): void => {
    event.persist();
    setSearchGroupName(event.target.value);
  };

  const onTreatmentStatusChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ): void => {
    event.persist();
    setFilterVulnerabilitiesTable(
      (value): IFilterTodosSet => ({
        ...value,
        treatmentCurrentStatus: event.target.value,
      })
    );
  };

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

  const filterTreatmentVulnerabilities: IVulnRowAttr[] = filterTreatment(
    vulnerabilities,
    filterVulnerabilitiesTable.treatment
  );

  const filterGroupNameVulnerabilities: IVulnRowAttr[] = filterSelect(
    vulnerabilities,
    searchGroupName,
    "groupName"
  );

  const filterTreatmentCurrentStatusVulnerabilities: IVulnRowAttr[] =
    filterTreatmentCurrentStatus(
      vulnerabilities,
      filterVulnerabilitiesTable.treatmentCurrentStatus
    );

  function clearFilters(): void {
    setFilterVulnerabilitiesTable(
      (): IFilterTodosSet => ({
        tag: "",
        treatment: "",
        treatmentCurrentStatus: "",
      })
    );
    setSearchTextFilter("");
    setSearchGroupName("");
  }

  const resultVulnerabilities: IVulnRowAttr[] = _.intersection(
    filterSearchTextVulnerabilities,
    filterTagVulnerabilities,
    filterTreatmentVulnerabilities,
    filterTreatmentCurrentStatusVulnerabilities,
    filterGroupNameVulnerabilities
  );

  const vulnerabilitiesGroupNameArray = vulnerabilities.map(
    (vulnerability: IVulnRowAttr): string[] => [
      vulnerability.groupName,
      vulnerability.groupName,
    ]
  );
  const groupNameOptions = Object.fromEntries(
    _.sortBy(vulnerabilitiesGroupNameArray, (arr): string => arr[0])
  );

  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: filterVulnerabilitiesTable.treatment,
      onChangeSelect: onTreatmentChange,
      placeholder: "Treatment",
      /* eslint-disable sort-keys */
      selectOptions: {
        NEW: "searchFindings.tabDescription.treatment.new",
        IN_PROGRESS: "searchFindings.tabDescription.treatment.inProgress",
        ACCEPTED: "searchFindings.tabDescription.treatment.accepted",
        ACCEPTED_UNDEFINED:
          "searchFindings.tabDescription.treatment.acceptedUndefined",
      },
      /* eslint-enable sort-keys */
      tooltipId: "searchFindings.tabVuln.vulnTable.treatmentsTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.vulnTable.treatmentsTooltip",
      type: "select",
    },
    {
      defaultValue: filterVulnerabilitiesTable.treatmentCurrentStatus,
      onChangeSelect: onTreatmentStatusChange,
      placeholder: "Treatment Acceptance",
      selectOptions: {
        false: "Accepted",
        true: "Pending",
      },
      tooltipId: "searchFindings.tabVuln.treatmentStatus.id",
      tooltipMessage: "searchFindings.tabVuln.treatmentStatus",
      type: "select",
    },
    {
      defaultValue: filterVulnerabilitiesTable.tag,
      onChangeInput: onTagChange,
      placeholder: "searchFindings.tabVuln.searchTag",
      tooltipId: "searchFindings.tabVuln.tagTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.tagTooltip",
      type: "text",
    },
    {
      defaultValue: searchGroupName,
      onChangeSelect: onSearchGroupNameChange,
      placeholder: t("taskContainer.filters.groupName.placeholder"),
      selectOptions: groupNameOptions,
      tooltipId: "taskContainer.filters.groupName.tooltip.id",
      tooltipMessage: "taskContainer.filters.groupName.tooltip",
      type: "select",
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
