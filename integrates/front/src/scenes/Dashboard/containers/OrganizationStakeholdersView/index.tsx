import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Glyphicon } from "react-bootstrap";
import { useParams } from "react-router";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { timeFromNow } from "components/DataTableNext/formatters";
import { IHeaderConfig } from "components/DataTableNext/types";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/NewTooltipWrapper";
import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import {
  ADD_STAKEHOLDER_MUTATION,
  EDIT_STAKEHOLDER_MUTATION,
  GET_ORGANIZATION_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/containers/OrganizationStakeholdersView/queries";
import {
  IAddStakeholderAttrs,
  IEditStakeholderAttrs,
  IGetStakeholdersAttrs,
  IOrganizationStakeholders,
  IRemoveStakeholderAttrs,
  IStakeholderAttrs,
} from "scenes/Dashboard/containers/OrganizationStakeholdersView/types";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { authContext, IAuthContext } from "utils/auth";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const tableHeaders: IHeaderConfig[] = [
  {
    dataField: "email",
    header: translate.t("search_findings.users_table.usermail"),
    width: "38%",
  },
  {
    dataField: "role",
    formatter: (value: string) => translate.t(
      `userModal.roles.${value}`,
      { defaultValue: "-" },
    ),
    header: translate.t("search_findings.users_table.userRole"),
    width: "15%",
  },
  {
    dataField: "phoneNumber",
    header: translate.t("search_findings.users_table.phoneNumber"),
    width: "15%",
  },
  {
    dataField: "firstLogin",
    header: translate.t("search_findings.users_table.firstlogin"),
    width: "15%",
  },
  {
    dataField: "lastLogin",
    formatter: timeFromNow,
    header: translate.t("search_findings.users_table.lastlogin"),
    width: "15%",
  },
];

const handleMtError: (mtError: ApolloError) => void = (mtError: ApolloError): void => {
  mtError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - Email is not valid":
        msgError(translate.t("validations.email"));
        break;
      case "Exception - Invalid field in form":
        msgError(translate.t("validations.invalidValueInField"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalid_char"));
        break;
      case "Exception - Invalid phone number in form":
        msgError(translate.t("validations.invalidPhoneNumberInField"));
        break;
      case "Exception - Invalid email address in form":
        msgError(translate.t("validations.invalidEmailInField"));
        break;
      default:
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred adding user to organization", mtError);
    }
  });
};

const organizationStakeholders: React.FC<IOrganizationStakeholders> =
  (props: IOrganizationStakeholders): JSX.Element => {
  const { organizationId } = props;
  const { organizationName } = useParams<{ organizationName: string }>();
  const { userName }: IAuthContext = React.useContext(authContext);
  const [pageSize, setPageSize] = React.useState<number>(10);
  const [pageIndex, setPageIndex] = React.useState<number>(1);

  // State management
  const [currentRow, setCurrentRow] = React.useState<Dictionary<string>>({});
  const [isStakeholderModalOpen, setStakeholderModalOpen] = React.useState(false);
  const [stakeholderModalAction, setStakeholderModalAction] = React.useState<"add" | "edit">("add");

  const openAddStakeholderModal: (() => void) = (): void => {
    setStakeholderModalAction("add");
    setStakeholderModalOpen(true);
  };
  const openEditStakeholderModal: (() => void) = (): void => {
    setStakeholderModalAction("edit");
    setStakeholderModalOpen(true);
  };
  const closeStakeholderModal: (() => void) = (): void => {
    setStakeholderModalOpen(false);
  };

  // GraphQL Operations
  const doRefetchStakeholders: ((page?: number, editedStakeholderEmail?: string) => void) =
    (page?: number, editedStakeholderEmail?: string): void => {
      void refetchStakeholders({
        updateQuery: (prev: IGetStakeholdersAttrs, options: Record<string, unknown>): IGetStakeholdersAttrs => {
          const fetchMoreResult: IGetStakeholdersAttrs = options.fetchMoreResult as IGetStakeholdersAttrs;
          if (_.isEmpty(fetchMoreResult)) {
            return prev;
          }

          const newStakeholders: IStakeholderAttrs[] = fetchMoreResult.organization.stakeholders.stakeholders;
          const currentStakeholders: IStakeholderAttrs[] = !_.isUndefined(editedStakeholderEmail) ?
            prev.organization.stakeholders.stakeholders.map((stakeholder: IStakeholderAttrs) => {
              const editedStakeholder: IStakeholderAttrs | undefined =
                newStakeholders.find((newStakeholder: IStakeholderAttrs): boolean =>
                  newStakeholder.email === stakeholder.email && newStakeholder.email === editedStakeholderEmail,
                );

              return !_.isUndefined(editedStakeholder) ? editedStakeholder : stakeholder;
            }) : prev.organization.stakeholders.stakeholders;

          const newStakeholdersList: IStakeholderAttrs[] =
            [...currentStakeholders, ...newStakeholders].reduce(
              (list: IStakeholderAttrs[], stakeholder: IStakeholderAttrs) => {
                if (!list.some(
                  (currentStakeholder: IStakeholderAttrs) => currentStakeholder.email === stakeholder.email)
                ) {
                  list.push(stakeholder);
                }

                return list;
              },
              [],
            );

          return {
            ...prev,
            organization: {
              __typename: "Organization",
              ...currentStakeholders,
              stakeholders: {
                __typename: "GetStakeholdersPayload",
                numPages: prev.organization.stakeholders.numPages,
                stakeholders: newStakeholdersList,
              },
            },
          };
        },
        variables: {
          organizationId,
          pageIndex: page,
          pageSize,
        },
      });
  };

  const { data, fetchMore: refetchStakeholders } = useQuery<IGetStakeholdersAttrs>(GET_ORGANIZATION_STAKEHOLDERS, {
    notifyOnNetworkStatusChange: true,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning(
          "An error occurred fetching organization stakeholders",
          error,
        );
      });
    },
    variables: {
      organizationId,
      pageIndex: 1,
      pageSize,
    },
  });

  const [grantStakeholderAccess] = useMutation(ADD_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IAddStakeholderAttrs): void => {
      if (mtResult.grantStakeholderOrganizationAccess.success) {
        doRefetchStakeholders(pageIndex);
        mixpanel.track("AddUserOrganzationAccess", { Organization: organizationName, User: userName });
        const { email } = mtResult.grantStakeholderOrganizationAccess.grantedStakeholder;
        msgSuccess(
          `${email} ${translate.t("organization.tabs.users.addButton.success")}`,
          translate.t("organization.tabs.users.successTitle"),
        );
      }
    },
    onError: handleMtError,
  });

  const [editStakeholder] = useMutation(EDIT_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IEditStakeholderAttrs): void => {
      if (mtResult.editStakeholderOrganization.success) {
        const { email } = mtResult.editStakeholderOrganization.modifiedStakeholder;
        doRefetchStakeholders(pageIndex, email);

        mixpanel.track("EditUserOrganizationAccess", { Organization: organizationName, User: userName });
        msgSuccess(
          `${email} ${translate.t("organization.tabs.users.editButton.success")}`,
          translate.t("organization.tabs.users.successTitle"),
        );
      }
    },
    onError: handleMtError,
  });

  const [removeStakeholderAccess, { loading: removing }] = useMutation(REMOVE_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IRemoveStakeholderAttrs): void => {
      if (mtResult.removeStakeholderOrganizationAccess.success && !_.isUndefined(data)) {
        const stakeholders: IStakeholderAttrs[] = data.organization.stakeholders.stakeholders;
        const removeIndex: number = stakeholders.map(
          (stakeholder: IStakeholderAttrs) => stakeholder.email)
          .indexOf(currentRow.email);
        stakeholders.splice(removeIndex, 1);

        mixpanel.track("RemoveUserOrganizationAccess", { Organization: organizationName, User: userName });
        msgSuccess(
          `${currentRow.email} ${translate.t("organization.tabs.users.removeButton.success")}`,
          translate.t("organization.tabs.users.successTitle"),
        );
        setCurrentRow({});
      }
    },
    onError: (removeError: ApolloError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred removing stakeholder", removeError);
    },
  });

  // Auxiliary elements
  const handleSubmit: ((values: IStakeholderAttrs) => void) = (values: IStakeholderAttrs): void => {
    closeStakeholderModal();
    if (stakeholderModalAction === "add") {
      void grantStakeholderAccess({ variables: {
        ...values,
        organizationId,
      } });
    } else {
      void editStakeholder({ variables: {
        ...values,
        organizationId,
      } });
    }
  };

  const handleRemoveStakeholder: (() => void) = (): void => {
    void removeStakeholderAccess({ variables: {
      organizationId,
      userEmail: currentRow.email,
    } });
    setStakeholderModalAction("add");
  };

  const onPageChange: ((page: number) => void) = (page: number): void => {
    doRefetchStakeholders(page);
    setPageIndex(page);
  };

  const onSizePerPageChange: ((pageSize: number, _: number) => void) =
  // tslint:disable-next-line: no-shadowed-variable
    (pageSize: number, _: number): void => {
      setPageSize(pageSize);
    };

  const listStakeholders: IStakeholderAttrs[] =
    !_.isUndefined(data) && !_.isEmpty(data) ? data?.organization.stakeholders.stakeholders : [];
  const numPages: number = !_.isUndefined(data) && !_.isEmpty(data) ? data?.organization.stakeholders.numPages : 1;

  return (
    <React.StrictMode>
      <div id="users" className="tab-pane cont active" >
        <Row>
          <Col100>
            <Row>
              <Col100>
                <ButtonToolbar>
                    <TooltipWrapper
                      displayClass={"dib"}
                      id={"organization.tabs.users.addButton.tooltip.btn"}
                      message={translate.t("organization.tabs.users.addButton.tooltip")}
                    >
                      <Button id="addUser" onClick={openAddStakeholderModal}>
                        <Glyphicon glyph="plus" />
                        &nbsp;{translate.t("organization.tabs.users.addButton.text")}
                      </Button>
                    </TooltipWrapper>
                    <TooltipWrapper
                      displayClass={"dib"}
                      id={"organization.tabs.users.editButton.tooltip.btn"}
                      message={translate.t("organization.tabs.users.editButton.tooltip")}
                    >
                      <Button id="editUser" onClick={openEditStakeholderModal} disabled={_.isEmpty(currentRow)}>
                        <FluidIcon icon="edit" />
                        &nbsp;{translate.t("organization.tabs.users.editButton.text")}
                      </Button>
                    </TooltipWrapper>
                    <TooltipWrapper
                      displayClass={"dib"}
                      id={"organization.tabs.users.removeButton.tooltip.btn"}
                      message={translate.t("organization.tabs.users.removeButton.tooltip")}
                    >
                      <Button
                        id="removeUser"
                        onClick={handleRemoveStakeholder}
                        disabled={_.isEmpty(currentRow) || removing}
                      >
                        <Glyphicon glyph="minus" />
                        &nbsp;{translate.t("organization.tabs.users.removeButton.text")}
                      </Button>
                    </TooltipWrapper>
                </ButtonToolbar>
              </Col100>
            </Row>
            <br />
            <Row>
              <Col100>
                <DataTableNext
                  id="tblUsers"
                  bordered={true}
                  dataset={listStakeholders}
                  exportCsv={true}
                  headers={tableHeaders}
                  numPages={numPages}
                  onPageChange={onPageChange}
                  pageSize={pageSize}
                  onSizePerPageChange={onSizePerPageChange}
                  search={true}
                  striped={true}
                  selectionMode={{
                    clickToSelect: true,
                    mode: "radio",
                    onSelect: setCurrentRow,
                  }}
                />
              </Col100>
            </Row>
          </Col100>
        </Row>
        <AddUserModal
          action={stakeholderModalAction}
          editTitle={translate.t("organization.tabs.users.modalEditTitle")}
          initialValues={stakeholderModalAction === "edit" ? currentRow : {}}
          onSubmit={handleSubmit}
          open={isStakeholderModalOpen}
          onClose={closeStakeholderModal}
          organizationId={organizationId}
          title={translate.t("organization.tabs.users.modalAddTitle")}
          type="organization"
        />
      </div>
    </React.StrictMode>
    );
};

export { organizationStakeholders as OrganizationStakeholders };
