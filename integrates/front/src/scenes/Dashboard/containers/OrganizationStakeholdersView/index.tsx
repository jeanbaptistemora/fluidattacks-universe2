import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faPlus,
  faTrashAlt,
  faUserEdit,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router-dom";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { timeFromNow } from "components/DataTableNext/formatters";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { filterSearchText } from "components/DataTableNext/utils";
import { TooltipWrapper } from "components/TooltipWrapper";
import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import {
  ADD_STAKEHOLDER_MUTATION,
  GET_ORGANIZATION_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
  UPDATE_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/containers/OrganizationStakeholdersView/queries";
import type {
  IAddStakeholderAttrs,
  IGetOrganizationStakeholders,
  IOrganizationStakeholders,
  IRemoveStakeholderAttrs,
  IStakeholderAttrs,
  IUpdateStakeholderAttrs,
} from "scenes/Dashboard/containers/OrganizationStakeholdersView/types";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const tableHeaders: IHeaderConfig[] = [
  {
    dataField: "email",
    header: translate.t("searchFindings.usersTable.usermail"),
    width: "40%",
  },
  {
    dataField: "role",
    formatter: (value: string): string =>
      translate.t(`userModal.roles.${_.camelCase(value)}`, {
        defaultValue: "-",
      }),
    header: translate.t("searchFindings.usersTable.userRole"),
    width: "20%",
  },
  {
    dataField: "firstLogin",
    header: translate.t("searchFindings.usersTable.firstlogin"),
    width: "20%",
  },
  {
    dataField: "lastLogin",
    formatter: timeFromNow,
    header: translate.t("searchFindings.usersTable.lastlogin"),
    width: "20%",
  },
];

const handleMtError: (mtError: ApolloError) => void = (
  mtError: ApolloError
): void => {
  mtError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - Email is not valid":
        msgError(translate.t("validations.email"));
        break;
      case "Exception - This role can only be granted to Fluid Attacks users":
        msgError(translate.t("validations.userIsNotFromFluidAttacks"));
        break;
      case "Exception - Invalid field in form":
        msgError(translate.t("validations.invalidValueInField"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalidChar"));
        break;
      case "Exception - Invalid email address in form":
        msgError(translate.t("validations.invalidEmailInField"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred adding user to organization",
          mtError
        );
    }
  });
};

const OrganizationStakeholders: React.FC<IOrganizationStakeholders> = (
  props: IOrganizationStakeholders
): JSX.Element => {
  const { organizationId } = props;
  const { organizationName } = useParams<{ organizationName: string }>();

  // State management
  const [currentRow, setCurrentRow] = useState<Dictionary<string>>({});
  const [isStakeholderModalOpen, setStakeholderModalOpen] = useState(false);
  const [stakeholderModalAction, setStakeholderModalAction] = useState<
    "add" | "edit"
  >("add");
  const [searchTextFilter, setSearchTextFilter] = useState("");

  const openAddStakeholderModal: () => void = useCallback((): void => {
    setStakeholderModalAction("add");
    setStakeholderModalOpen(true);
  }, []);
  const openEditStakeholderModal: () => void = useCallback((): void => {
    setStakeholderModalAction("edit");
    setStakeholderModalOpen(true);
  }, []);
  const closeStakeholderModal: () => void = useCallback((): void => {
    setStakeholderModalOpen(false);
  }, []);

  // GraphQL Operations
  const { data, refetch: refetchStakeholders } =
    useQuery<IGetOrganizationStakeholders>(GET_ORGANIZATION_STAKEHOLDERS, {
      notifyOnNetworkStatusChange: true,
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred fetching organization stakeholders",
            error
          );
        });
      },
      variables: { organizationId },
    });

  const [grantStakeholderAccess] = useMutation(ADD_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IAddStakeholderAttrs): void => {
      if (mtResult.grantStakeholderOrganizationAccess.success) {
        void refetchStakeholders();
        track("AddUserOrganzationAccess", {
          Organization: organizationName,
        });
        const { email } =
          mtResult.grantStakeholderOrganizationAccess.grantedStakeholder;
        msgSuccess(
          `${email} ${translate.t(
            "organization.tabs.users.addButton.success"
          )}`,
          translate.t("organization.tabs.users.successTitle")
        );
      }
    },
    onError: handleMtError,
  });

  const [updateStakeholder] = useMutation(UPDATE_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IUpdateStakeholderAttrs): void => {
      if (mtResult.updateOrganizationStakeholder.success) {
        const { email } =
          mtResult.updateOrganizationStakeholder.modifiedStakeholder;
        void refetchStakeholders();

        track("EditUserOrganizationAccess", {
          Organization: organizationName,
        });
        msgSuccess(
          `${email} ${translate.t(
            "organization.tabs.users.editButton.success"
          )}`,
          translate.t("organization.tabs.users.successTitle")
        );
      }
    },
    onError: handleMtError,
  });

  const [removeStakeholderAccess, { loading: removing }] = useMutation(
    REMOVE_STAKEHOLDER_MUTATION,
    {
      onCompleted: (mtResult: IRemoveStakeholderAttrs): void => {
        if (mtResult.removeStakeholderOrganizationAccess.success) {
          void refetchStakeholders();

          track("RemoveUserOrganizationAccess", {
            Organization: organizationName,
          });
          msgSuccess(
            `${currentRow.email} ${translate.t(
              "organization.tabs.users.removeButton.success"
            )}`,
            translate.t("organization.tabs.users.successTitle")
          );
          setCurrentRow({});
        }
      },
      onError: (removeError: ApolloError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred removing stakeholder", removeError);
      },
    }
  );

  // Auxiliary elements
  const handleSubmit: (values: IStakeholderAttrs) => void = useCallback(
    (values: IStakeholderAttrs): void => {
      closeStakeholderModal();
      if (stakeholderModalAction === "add") {
        void grantStakeholderAccess({
          variables: {
            ...values,
            organizationId,
          },
        });
      } else {
        void updateStakeholder({
          variables: {
            ...values,
            organizationId,
          },
        });
      }
    },
    [
      closeStakeholderModal,
      updateStakeholder,
      grantStakeholderAccess,
      organizationId,
      stakeholderModalAction,
    ]
  );

  const handleRemoveStakeholder: () => void = useCallback((): void => {
    void removeStakeholderAccess({
      variables: {
        organizationId,
        userEmail: currentRow.email,
      },
    });
    setStakeholderModalAction("add");
  }, [currentRow.email, organizationId, removeStakeholderAccess]);

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }

  const stakeholdersList: IStakeholderAttrs[] =
    _.isUndefined(data) || _.isEmpty(data)
      ? []
      : data.organization.stakeholders;

  const filterSearchtextResult: IStakeholderAttrs[] = filterSearchText(
    stakeholdersList,
    searchTextFilter
  );

  return (
    <React.StrictMode>
      <div className={"tab-pane cont active"} id={"users"}>
        <Row>
          <Col100>
            <Row>
              <Col100>
                <DataTableNext
                  bordered={true}
                  customSearch={{
                    customSearchDefault: searchTextFilter,
                    isCustomSearchEnabled: true,
                    onUpdateCustomSearch: onSearchTextChange,
                    position: "right",
                  }}
                  dataset={filterSearchtextResult}
                  exportCsv={true}
                  extraButtons={
                    <Row>
                      <ButtonToolbar>
                        <TooltipWrapper
                          displayClass={"dib"}
                          id={"organization.tabs.users.addButton.tooltip.btn"}
                          message={translate.t(
                            "organization.tabs.users.addButton.tooltip"
                          )}
                        >
                          <Button
                            id={"addUser"}
                            onClick={openAddStakeholderModal}
                          >
                            <FontAwesomeIcon icon={faPlus} />
                            &nbsp;
                            {translate.t(
                              "organization.tabs.users.addButton.text"
                            )}
                          </Button>
                        </TooltipWrapper>
                        <TooltipWrapper
                          displayClass={"dib"}
                          id={"organization.tabs.users.editButton.tooltip.btn"}
                          message={translate.t(
                            "organization.tabs.users.editButton.tooltip"
                          )}
                        >
                          <Button
                            disabled={_.isEmpty(currentRow)}
                            id={"editUser"}
                            onClick={openEditStakeholderModal}
                          >
                            <FontAwesomeIcon icon={faUserEdit} />
                            &nbsp;
                            {translate.t(
                              "organization.tabs.users.editButton.text"
                            )}
                          </Button>
                        </TooltipWrapper>
                        <TooltipWrapper
                          displayClass={"dib"}
                          id={
                            "organization.tabs.users.removeButton.tooltip.btn"
                          }
                          message={translate.t(
                            "organization.tabs.users.removeButton.tooltip"
                          )}
                        >
                          <Button
                            disabled={_.isEmpty(currentRow) || removing}
                            id={"removeUser"}
                            onClick={handleRemoveStakeholder}
                          >
                            <FontAwesomeIcon icon={faTrashAlt} />
                            &nbsp;
                            {translate.t(
                              "organization.tabs.users.removeButton.text"
                            )}
                          </Button>
                        </TooltipWrapper>
                      </ButtonToolbar>
                    </Row>
                  }
                  headers={tableHeaders}
                  id={"tblUsers"}
                  pageSize={10}
                  search={false}
                  selectionMode={{
                    clickToSelect: true,
                    mode: "radio",
                    onSelect: setCurrentRow,
                  }}
                  striped={true}
                />
              </Col100>
            </Row>
          </Col100>
        </Row>
        <AddUserModal
          action={stakeholderModalAction}
          editTitle={translate.t("organization.tabs.users.modalEditTitle")}
          initialValues={stakeholderModalAction === "edit" ? currentRow : {}}
          onClose={closeStakeholderModal}
          onSubmit={handleSubmit}
          open={isStakeholderModalOpen}
          organizationId={organizationId}
          title={translate.t("organization.tabs.users.modalAddTitle")}
          type={"organization"}
        />
      </div>
    </React.StrictMode>
  );
};

export { OrganizationStakeholders };
