import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { FluidIcon } from "components/FluidIcon";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Logger } from "utils/logger";
import { TooltipWrapper } from "components/TooltipWrapper";
import _ from "lodash";
import { timeFromNow } from "components/DataTableNext/formatters";
import { track } from "mixpanel-browser";
import { translate } from "utils/translations/translate";
import { useParams } from "react-router";
import {
  ADD_STAKEHOLDER_MUTATION,
  EDIT_STAKEHOLDER_MUTATION,
  GET_ORGANIZATION_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/containers/OrganizationStakeholdersView/queries";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import type {
  IAddStakeholderAttrs,
  IEditStakeholderAttrs,
  IOrganizationStakeholders,
  IRemoveStakeholderAttrs,
  IStakeholderAttrs,
} from "scenes/Dashboard/containers/OrganizationStakeholdersView/types";
import React, { useCallback, useState } from "react";
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { msgError, msgSuccess } from "utils/notifications";
import { useMutation, useQuery } from "@apollo/react-hooks";

const tableHeaders: IHeaderConfig[] = [
  {
    dataField: "email",
    header: translate.t("searchFindings.usersTable.usermail"),
    width: "38%",
  },
  {
    dataField: "role",
    formatter: (value: string): string =>
      translate.t(`userModal.roles.${_.camelCase(value)}`, {
        defaultValue: "-",
      }),
    header: translate.t("searchFindings.usersTable.userRole"),
    width: "15%",
  },
  {
    dataField: "phoneNumber",
    header: translate.t("searchFindings.usersTable.phoneNumber"),
    width: "15%",
  },
  {
    dataField: "firstLogin",
    header: translate.t("searchFindings.usersTable.firstlogin"),
    width: "15%",
  },
  {
    dataField: "lastLogin",
    formatter: timeFromNow,
    header: translate.t("searchFindings.usersTable.lastlogin"),
    width: "15%",
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
      case "Exception - Invalid field in form":
        msgError(translate.t("validations.invalidValueInField"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalidChar"));
        break;
      case "Exception - Invalid phone number in form":
        msgError(translate.t("validations.invalidPhoneNumberInField"));
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
  const { data, refetch: refetchStakeholders } = useQuery(
    GET_ORGANIZATION_STAKEHOLDERS,
    {
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
    }
  );

  const [grantStakeholderAccess] = useMutation(ADD_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IAddStakeholderAttrs): void => {
      if (mtResult.grantStakeholderOrganizationAccess.success) {
        void refetchStakeholders();
        track("AddUserOrganzationAccess", {
          Organization: organizationName,
        });
        const {
          email,
        } = mtResult.grantStakeholderOrganizationAccess.grantedStakeholder;
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

  const [editStakeholder] = useMutation(EDIT_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IEditStakeholderAttrs): void => {
      if (mtResult.editStakeholderOrganization.success) {
        const {
          email,
        } = mtResult.editStakeholderOrganization.modifiedStakeholder;
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
        void editStakeholder({
          variables: {
            ...values,
            organizationId,
          },
        });
      }
    },
    [
      closeStakeholderModal,
      editStakeholder,
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

  const stakeholdersList: IStakeholderAttrs[] =
    _.isUndefined(data) || _.isEmpty(data)
      ? []
      : data.organization.stakeholders; // eslint-disable-line @typescript-eslint/no-unsafe-member-access

  return (
    <React.StrictMode>
      <div className={"tab-pane cont active"} id={"users"}>
        <Row>
          <Col100>
            <Row>
              <Col100>
                <ButtonToolbar>
                  <TooltipWrapper
                    displayClass={"dib"}
                    id={"organization.tabs.users.addButton.tooltip.btn"}
                    message={translate.t(
                      "organization.tabs.users.addButton.tooltip"
                    )}
                  >
                    <Button id={"addUser"} onClick={openAddStakeholderModal}>
                      <FontAwesomeIcon icon={faPlus} />
                      &nbsp;
                      {translate.t("organization.tabs.users.addButton.text")}
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
                      <FluidIcon icon={"edit"} />
                      &nbsp;
                      {translate.t("organization.tabs.users.editButton.text")}
                    </Button>
                  </TooltipWrapper>
                  <TooltipWrapper
                    displayClass={"dib"}
                    id={"organization.tabs.users.removeButton.tooltip.btn"}
                    message={translate.t(
                      "organization.tabs.users.removeButton.tooltip"
                    )}
                  >
                    <Button
                      disabled={_.isEmpty(currentRow) || removing}
                      id={"removeUser"}
                      onClick={handleRemoveStakeholder}
                    >
                      <FontAwesomeIcon icon={faMinus} />
                      &nbsp;
                      {translate.t("organization.tabs.users.removeButton.text")}
                    </Button>
                  </TooltipWrapper>
                </ButtonToolbar>
              </Col100>
            </Row>
            <br />
            <Row>
              <Col100>
                <DataTableNext
                  bordered={true}
                  dataset={stakeholdersList}
                  exportCsv={true}
                  headers={tableHeaders}
                  id={"tblUsers"}
                  pageSize={10}
                  search={true}
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
