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
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import type { IFilterProps } from "components/Table/types";
import {
  filterDateRange,
  filterSearchText,
  filterSelect,
  filterText,
} from "components/Table/utils";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateDescription } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import {
  filterTreatment,
  filterTreatmentCurrentStatus,
  formatVulnerabilitiesTreatment,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { ReattackVulnerabilities } from "scenes/Dashboard/containers/Tasks/ActionsButtons/ReattackVulnerabilities/index";
import type {
  IAction,
  IFilterTodosSet,
  IGroupAction,
  ITasksContent,
} from "scenes/Dashboard/containers/Tasks/types";
import { filteredContinuousVulnerabilitiesOnReattackIds } from "scenes/Dashboard/containers/Tasks/utils";
import { EditButton } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons/EditButton";
import type { IModalConfig } from "scenes/Dashboard/containers/VulnerabilitiesView/types";
import type { IOrganizationGroups } from "scenes/Dashboard/types";
import { ButtonToolbarRow } from "styles/styledComponents";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { useStoredState, useTabTracking } from "utils/hooks";
import { msgError } from "utils/notifications";

export const TasksContent: React.FC<ITasksContent> = ({
  userData,
  meVulnerabilitiesAssigned,
  setUserRole,
  refetchVulnerabilitiesAssigned,
}: ITasksContent): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRetrieveHacker: boolean = permissions.can(
    "api_resolvers_vulnerability_hacker_resolve"
  );

  const [isEditing, setEditing] = useState(false);
  const [iscurrentOpen, setCurrentOpen] = useState<boolean[]>([]);
  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [searchGroupName, setSearchGroupName] = useState("");
  const [isReattacking, setReattacking] = useState(false);
  const [isOpen, setOpen] = useState(false);
  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("todosLocationsCustomFilters", false);
  const [filterVulnerabilitiesTable, setFilterVulnerabilitiesTable] =
    useStoredState<IFilterTodosSet>(
      "filterTodosVulnerabilitiesSet",
      {
        reportDateRange: { max: "", min: "" },
        tag: "",
        treatment: "",
        treatmentCurrentStatus: "",
        verification: "",
      },
      localStorage
    );
  const attributesContext: PureAbility<string> = useContext(authzGroupContext);
  const permissionsContext: PureAbility<string> = useContext(
    authzPermissionsContext
  );

  useTabTracking("Todos");

  const groups = useMemo(
    (): IOrganizationGroups["groups"] =>
      userData === undefined
        ? []
        : userData.me.organizations.reduce(
            (
              previousValue: IOrganizationGroups["groups"],
              currentValue
            ): IOrganizationGroups["groups"] => [
              ...previousValue,
              ...currentValue.groups,
            ],
            []
          ),
    [userData]
  );

  const vulnerabilities: IVulnRowAttr[] = useMemo(
    (): IVulnRowAttr[] =>
      formatVulnerabilitiesTreatment(
        meVulnerabilitiesAssigned === undefined || userData === undefined
          ? []
          : meVulnerabilitiesAssigned.me.vulnerabilitiesAssigned
      ),
    [meVulnerabilitiesAssigned, userData]
  );

  const vulnerabilitesGroupName: string[] = useMemo(
    (): string[] =>
      Array.from(
        new Set(
          vulnerabilities.map((vulnerability: IVulnRowAttr): string =>
            vulnerability.groupName.toLowerCase()
          )
        )
      ),
    [vulnerabilities]
  );

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
      const groupsServicesAttributes: IOrganizationGroups["groups"] =
        userData.me.organizations.reduce(
          (
            previousValue: IOrganizationGroups["groups"],
            currentValue
          ): IOrganizationGroups["groups"] => [
            ...previousValue,
            ...currentValue.groups.filter((group): boolean =>
              vulnerabilitesGroupName.includes(group.name.toLowerCase())
            ),
          ],
          []
        );
      const currentAttributes: string[] = Array.from(
        new Set(
          groupsServicesAttributes.reduce(
            (previous: string[], current): string[] => [
              ...previous,
              ...current.serviceAttributes,
            ],
            []
          )
        )
      );
      if (currentAttributes.length > 0) {
        attributesContext.update(
          currentAttributes.map((action: string): IAction => ({ action }))
        );
      }
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
    vulnerabilitesGroupName,
    setUserRole,
  ]);

  const [modalConfig, setModalConfig] = useState<IModalConfig>({
    clearSelected: (): void => undefined,
    selectedVulnerabilities: [],
  });

  const openRemediationModal: (
    vuls: IVulnRowAttr[],
    clearSelected: () => void
  ) => void = useCallback(
    (vulns: IVulnRowAttr[], clearSelected: () => void): void => {
      setModalConfig({
        clearSelected,
        selectedVulnerabilities: vulns,
      });
    },
    []
  );

  const refreshAssigned: () => void = useCallback(async (): Promise<void> => {
    await refetchVulnerabilitiesAssigned();
  }, [refetchVulnerabilitiesAssigned]);

  const onSearchTextChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      setSearchTextFilter(event.target.value);
    },
    []
  );

  const onTreatmentChange = useCallback(
    (event: React.ChangeEvent<HTMLSelectElement>): void => {
      event.persist();
      setFilterVulnerabilitiesTable(
        (value): IFilterTodosSet => ({
          ...value,
          treatment: event.target.value,
        })
      );
    },
    [setFilterVulnerabilitiesTable]
  );

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

  const onReportDateMaxChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    event.persist();
    setFilterVulnerabilitiesTable(
      (value): IFilterTodosSet => ({
        ...value,
        reportDateRange: {
          max: event.target.value,
          min:
            value.reportDateRange === undefined
              ? ""
              : value.reportDateRange.min,
        },
      })
    );
  };

  const onReportDateMinChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    event.persist();
    setFilterVulnerabilitiesTable(
      (value): IFilterTodosSet => ({
        ...value,
        reportDateRange: {
          max:
            value.reportDateRange === undefined
              ? ""
              : value.reportDateRange.max,
          min: event.target.value,
        },
      })
    );
  };

  const onVerificationChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ): void => {
    event.persist();
    setFilterVulnerabilitiesTable(
      (value): IFilterTodosSet => ({
        ...value,
        verification: event.target.value,
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

  const filterReportDateRangeVulnerabilities: IVulnRowAttr[] = filterDateRange(
    vulnerabilities,
    filterVulnerabilitiesTable.reportDateRange ?? { max: "", min: "" },
    "reportDate"
  );

  const filterVerificationVulnerabilities: IVulnRowAttr[] = filterSelect(
    vulnerabilities,
    filterVulnerabilitiesTable.verification ?? "",
    "verification"
  );

  const clearFilters = useCallback((): void => {
    setFilterVulnerabilitiesTable(
      (): IFilterTodosSet => ({
        reportDateRange: { max: "", min: "" },
        tag: "",
        treatment: "",
        treatmentCurrentStatus: "",
        verification: "",
      })
    );
    setSearchTextFilter("");
    setSearchGroupName("");
  }, [setFilterVulnerabilitiesTable]);

  const resultVulnerabilities: IVulnRowAttr[] = _.intersection(
    filterReportDateRangeVulnerabilities,
    filterSearchTextVulnerabilities,
    filterTagVulnerabilities,
    filterTreatmentVulnerabilities,
    filterTreatmentCurrentStatusVulnerabilities,
    filterGroupNameVulnerabilities,
    filterVerificationVulnerabilities
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
      placeholder: t("taskContainer.filters.treatment.placeholder"),
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
      placeholder: t("taskContainer.filters.treatmentAcceptance.placeholder"),
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
    {
      defaultValue: filterVulnerabilitiesTable.verification ?? "",
      onChangeSelect: onVerificationChange,
      placeholder: "Reattacks",
      selectOptions: {
        // eslint-disable-next-line camelcase
        On_hold: "searchFindings.tabVuln.onHold",
        Requested: "searchFindings.tabVuln.requested",
        Verified: "searchFindings.tabVuln.verified",
      },
      tooltipId: "searchFindings.tabVuln.vulnTable.reattacksTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.vulnTable.reattacksTooltip",
      type: "select",
    },
    {
      defaultValue: "",
      placeholder: t("taskContainer.filters.dateRange.placeholder"),
      rangeProps: {
        defaultValue: filterVulnerabilitiesTable.reportDateRange ?? {
          max: "",
          min: "",
        },
        onChangeMax: onReportDateMaxChange,
        onChangeMin: onReportDateMinChange,
      },
      tooltipId: "searchFindings.tabVuln.vulnTable.dateTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.vulnTable.dateTooltip",
      type: "dateRange",
    },
  ];
  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  const toggleEdit = useCallback((): void => {
    setCurrentOpen(
      Object.entries(
        _.groupBy(
          modalConfig.selectedVulnerabilities,
          (vuln: IVulnRowAttr): string => vuln.groupName
        )
      ).map((__, index: number): boolean => index === 0)
    );
    setEditing(!isEditing);
  }, [isEditing, modalConfig.selectedVulnerabilities]);

  const handleCloseUpdateModal = useCallback(
    (index: number): void => {
      setCurrentOpen((current: boolean[]): boolean[] => {
        const newCurrent = current.map(
          (isCurrentOpen: boolean, currentIndex: number): boolean =>
            currentIndex === index
              ? !isCurrentOpen
              : currentIndex === index + 1
              ? !isCurrentOpen
              : isCurrentOpen
        );
        if (
          newCurrent.every((isCurrentOpen: boolean): boolean => !isCurrentOpen)
        ) {
          setEditing(false);
          modalConfig.clearSelected();
        }

        return newCurrent;
      });
    },
    [modalConfig]
  );

  const toggleModal = useCallback((): void => {
    setOpen(true);
  }, []);
  const closeRemediationModal = useCallback((): void => {
    setOpen(false);
  }, []);
  const onReattack = useCallback((): void => {
    if (isReattacking) {
      setReattacking(!isReattacking);
    } else {
      const { selectedVulnerabilities } = modalConfig;
      const validVulnerabilitiesId: string[] =
        filteredContinuousVulnerabilitiesOnReattackIds(
          selectedVulnerabilities,
          groups
        );
      const newValidVulnerabilities: IVulnRowAttr[] = Array.from(
        new Set(
          selectedVulnerabilities.filter(
            (selectedVulnerability: IVulnRowAttr): boolean =>
              validVulnerabilitiesId.includes(selectedVulnerability.id)
          )
        )
      );
      if (selectedVulnerabilities.length > newValidVulnerabilities.length) {
        setReattacking(!isReattacking);
        msgError(t("searchFindings.tabVuln.errors.selectedVulnerabilities"));
      } else if (selectedVulnerabilities.length > 0) {
        setOpen(true);
        setReattacking(!isReattacking);
      } else {
        setReattacking(!isReattacking);
      }
    }
  }, [groups, isReattacking, modalConfig, t]);

  if (_.isUndefined(userData) || _.isEmpty(userData)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <div>
        <div>
          <VulnComponent
            canDisplayHacker={canRetrieveHacker}
            changePermissions={changePermissions}
            clearFiltersButton={clearFilters}
            customFilters={{
              customFiltersProps,
              hideResults: true,
              isCustomFilterEnabled,
              onUpdateEnableCustomFilter: handleUpdateCustomFilter,
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
              <ButtonToolbarRow>
                <Button
                  disabled={isEditing || isReattacking}
                  id={"refresh-assigned"}
                  onClick={refreshAssigned}
                  variant={"secondary"}
                >
                  <FontAwesomeIcon icon={faSyncAlt} />
                </Button>
                <ReattackVulnerabilities
                  areVulnerabilitiesReattacked={
                    resultVulnerabilities.filter(
                      (vuln): boolean =>
                        !vuln.remediated &&
                        filteredContinuousVulnerabilitiesOnReattackIds(
                          resultVulnerabilities,
                          groups
                        ).includes(vuln.id)
                    ).length === 0
                  }
                  areVulnsSelected={
                    modalConfig.selectedVulnerabilities.length > 0
                  }
                  isEditing={isEditing}
                  isOpen={isOpen}
                  isRequestingReattack={isReattacking}
                  onRequestReattack={onReattack}
                  openModal={toggleModal}
                />
                <EditButton
                  isDisabled={modalConfig.selectedVulnerabilities.length === 0}
                  isEditing={isEditing}
                  isFindingReleased={true}
                  isRequestingReattack={isReattacking}
                  isVerifying={false}
                  onEdit={toggleEdit}
                />
              </ButtonToolbarRow>
            }
            findingState={"open"}
            isEditing={false}
            isFindingReleased={true}
            isRequestingReattack={isReattacking}
            isVerifyingRequest={false}
            nonValidOnReattackVulnerabilities={Array.from(
              new Set(
                vulnerabilities.filter(
                  (vulnerability: IVulnRowAttr): boolean =>
                    !filteredContinuousVulnerabilitiesOnReattackIds(
                      vulnerabilities,
                      groups
                    ).includes(vulnerability.id)
                )
              )
            )}
            onVulnSelect={openRemediationModal}
            vulnerabilities={resultVulnerabilities}
          />
        </div>
      </div>
      {isOpen ? (
        <UpdateVerificationModal
          clearSelected={_.get(modalConfig, "clearSelected")}
          handleCloseModal={closeRemediationModal}
          isReattacking={isReattacking}
          isVerifying={false}
          setRequestState={onReattack}
          setVerifyState={onReattack}
          vulns={modalConfig.selectedVulnerabilities}
        />
      ) : undefined}
      {isEditing && modalConfig.selectedVulnerabilities.length > 0
        ? Object.entries(
            _.groupBy(
              modalConfig.selectedVulnerabilities,
              (vuln: IVulnRowAttr): string => vuln.groupName
            )
          ).map(
            (
              [vulnGroupName, vulnerabilitiesToUpdated]: [
                string,
                IVulnRowAttr[]
              ],
              index: number
            ): JSX.Element => {
              function onClose(): void {
                handleCloseUpdateModal(index);
              }

              return (
                <Modal
                  key={vulnGroupName}
                  onClose={onClose}
                  open={iscurrentOpen[index]}
                  title={t("searchFindings.tabDescription.editVuln")}
                >
                  <UpdateDescription
                    changePermissions={changePermissions}
                    findingId={""}
                    groupName={vulnGroupName}
                    handleClearSelected={_.get(modalConfig, "clearSelected")}
                    handleCloseModal={onClose}
                    isOpen={iscurrentOpen[index]}
                    vulnerabilities={vulnerabilitiesToUpdated}
                  />
                </Modal>
              );
            }
          )
        : undefined}
    </React.StrictMode>
  );
};
