/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Glyphicon } from "react-bootstrap";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { statusFormatter, timeFromNow } from "components/DataTableNext/formatters";
import { IHeaderConfig } from "components/DataTableNext/types";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import {
  ADD_STAKEHOLDER_MUTATION,
  EDIT_STAKEHOLDER_MUTATION,
  GET_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/containers/ProjectStakeholdersView/queries";
import {
  IAddStakeholderAttr,
  IEditStakeholderAttr,
  IGetStakeholdersAttrs,
  IProjectStakeholdersViewProps,
  IRemoveStakeholderAttr,
  IStakeholderAttrs,
} from "scenes/Dashboard/containers/ProjectStakeholdersView/types";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { authContext, IAuthContext } from "utils/auth";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const tableHeaders: IHeaderConfig[] = [
  {
    dataField: "email",
    header: translate.t("search_findings.users_table.usermail"),
    width: "33%",
  },
  {
    dataField: "role",
    formatter: (value: string) => translate.t(
      `userModal.roles.${value}`,
      { defaultValue: "-" },
    ),
    header: translate.t("search_findings.users_table.userRole"),
    width: "12%",
  },
  {
    dataField: "responsibility",
    header: translate.t("search_findings.users_table.userResponsibility"),
    width: "12%",
  },
  {
    dataField: "phoneNumber",
    header: translate.t("search_findings.users_table.phoneNumber"),
    width: "12%",
  },
  {
    dataField: "firstLogin",
    header: translate.t("search_findings.users_table.firstlogin"),
    width: "12%",
  },
  {
    dataField: "lastLogin",
    formatter: timeFromNow,
    header: translate.t("search_findings.users_table.lastlogin"),
    width: "12%",
  },
  {
    dataField: "invitationState",
    formatter: statusFormatter,
    header: translate.t("search_findings.users_table.invitation"),
    width: "7%",
  },
];

const projectStakeholdersView: React.FC<IProjectStakeholdersViewProps> =
  (props: IProjectStakeholdersViewProps): JSX.Element => {
  const { projectName } = props.match.params;
  const { userName }: IAuthContext = React.useContext(authContext);
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const [pageSize, setPageSize] = React.useState<number>(10);
  const [pageIndex, setPageIndex] = React.useState<number>(1);

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("ProjectUsers", { User: userName });
  };
  React.useEffect(onMount, []);

  // State management
  const [currentRow, setCurrentRow] = React.useState<Dictionary<string>>({});
  const [isUserModalOpen, setUserModalOpen] = React.useState(false);
  const [userModalAction, setuserModalAction] = React.useState<"add" | "edit">("add");
  const openAddUserModal: (() => void) = (): void => {
    setuserModalAction("add");
    setUserModalOpen(true);
  };
  const openEditUserModal: (() => void) = (): void => {
    setuserModalAction("edit");
    setUserModalOpen(true);
  };
  const closeUserModal: (() => void) = (): void => {
    setUserModalOpen(false);
  };

  // GraphQL operations
  const doRefetchStakeholders: ((page?: number, editedStakeholderEmail?: string) => void) =
    (page?: number, editedStakeholderEmail?: string): void => {
      void refetchStakeholders({
        updateQuery: (prev: IGetStakeholdersAttrs, options: Record<string, unknown>): IGetStakeholdersAttrs => {
          const fetchMoreResult: IGetStakeholdersAttrs = options.fetchMoreResult as IGetStakeholdersAttrs;
          if (_.isEmpty(fetchMoreResult)) {
            return prev;
          }

          const newStakeholders: IStakeholderAttrs[] = fetchMoreResult.project.stakeholders.stakeholders;
          const currentStakeholders: IStakeholderAttrs[] = !_.isUndefined(editedStakeholderEmail) ?
            prev.project.stakeholders.stakeholders.map((stakeholder: IStakeholderAttrs) => {
              const editedStakeholder: IStakeholderAttrs | undefined =
                newStakeholders.find((newStakeholder: IStakeholderAttrs): boolean =>
                  newStakeholder.email === stakeholder.email && newStakeholder.email === editedStakeholderEmail,
                );

              return !_.isUndefined(editedStakeholder) ? editedStakeholder : stakeholder;
            }) : prev.project.stakeholders.stakeholders;

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
            project: {
              __typename: "Project",
              ...currentStakeholders,
              stakeholders: {
                __typename: "GetStakeholdersPayload",
                numPages: prev.project.stakeholders.numPages,
                stakeholders: newStakeholdersList,
              },
            },
          };
        },
        variables: {
          pageIndex: page,
          pageSize,
          projectName,
        },
      });
  };

  const { data, fetchMore: refetchStakeholders } = useQuery<IGetStakeholdersAttrs>(GET_STAKEHOLDERS, {
    notifyOnNetworkStatusChange: true,
    onError: (error: ApolloError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred loading project stakeholders", error);
    },
    variables: {
      pageIndex: 1,
      pageSize,
      projectName,
    },
  });
  const [grantStakeholderAccess] = useMutation(ADD_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IAddStakeholderAttr): void => {
      if (mtResult.grantStakeholderAccess.success) {
        doRefetchStakeholders(pageIndex);
        mixpanel.track("AddUserAccess", { User: userName });
        const { email } = mtResult.grantStakeholderAccess.grantedStakeholder;
        msgSuccess(
          `${email} ${translate.t("search_findings.tab_users.success")}`,
          translate.t("search_findings.tab_users.title_success"),
        );
      }
    },
    onError: (grantError: ApolloError): void => {
      grantError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
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
          case "Exception - Groups without an active Fluid Attacks service "
            + "can not have Fluid Attacks staff":
            msgError(translate.t("validations.fluid_attacks_staff_without_fluid_attacks_service"));
            break;
          case "Exception - Groups with any active Fluid Attacks service "
            + "can only have Hackers provided by Fluid Attacks":
            msgError(translate.t("validations.no_fluid_attacks_hackers_in_fluid_attacks_service"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred adding stakeholder to project", grantError);
        }
      });
    },
  });

  const [editStakeholder] = useMutation(EDIT_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IEditStakeholderAttr): void => {
      if (mtResult.editStakeholder.success) {
        const { email } = mtResult.editStakeholder.modifiedStakeholder;
        doRefetchStakeholders(pageIndex, email);
        mixpanel.track("EditUserAccess", { User: userName });
        msgSuccess(
          translate.t("search_findings.tab_users.success_admin"),
          translate.t("search_findings.tab_users.title_success"),
        );
      }
    },
    onError: (editError: ApolloError): void => {
      editError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Invalid field in form":
            msgError(translate.t("validations.invalidValueInField"));
            break;
          case "Exception - Invalid characters":
            msgError(translate.t("validations.invalid_char"));
            break;
          case "Exception - Invalid phone number in form":
            msgError(translate.t("validations.invalidPhoneNumberInField"));
            break;
          case "Exception - Groups without an active Fluid Attacks service "
            + "can not have Fluid Attacks staff":
            msgError(translate.t("validations.fluid_attacks_staff_without_fluid_attacks_service"));
            break;
          case "Exception - Groups with any active Fluid Attacks service "
            + "can only have Hackers provided by Fluid Attacks":
            msgError(translate.t("validations.no_fluid_attacks_hackers_in_fluid_attacks_service"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred editing user", editError);
        }
      });
    },
  });

  const [removeStakeholderAccess, { loading: removing }] = useMutation(REMOVE_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IRemoveStakeholderAttr): void => {
      if (mtResult.removeStakeholderAccess.success && !_.isUndefined(data)) {
        data.project.stakeholders.stakeholders.filter(
          (stakeholder: IStakeholderAttrs) => stakeholder.email !== currentRow.email);

        mixpanel.track("RemoveUserAccess", { User: userName });
        const { removedEmail } = mtResult.removeStakeholderAccess;
        msgSuccess(
          `${removedEmail} ${translate.t("search_findings.tab_users.success_delete")}`,
          translate.t("search_findings.tab_users.title_success"),
        );
      }
    },
    onError: (removeError: ApolloError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred removing user", removeError);
    },
  });

  const handleSubmit: ((values: IStakeholderAttrs) => void) = (values: IStakeholderAttrs): void => {
    closeUserModal();
    if (userModalAction === "add") {
      void grantStakeholderAccess({ variables: {
          ...values,
          projectName,
      } });
    } else {
      void editStakeholder({ variables: {
          ...values,
          projectName,
      } });
    }
  };

  const handleRemoveUser: (() => void) = (): void => {
    void removeStakeholderAccess({ variables: { projectName, userEmail: currentRow.email } });
    setCurrentRow({});
    setuserModalAction("add");
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

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const listStakeholders: IStakeholderAttrs[] =
    !_.isUndefined(data) && !_.isEmpty(data) ? data?.project.stakeholders.stakeholders : [];
  const numPages: number = !_.isUndefined(data) && !_.isEmpty(data) ? data?.project.stakeholders.numPages : 1;

  return (
    <React.StrictMode>
      <div id="users" className="tab-pane cont active" >
        <Row>
          <Col100>
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Can do="backend_api_mutations_grant_stakeholder_access_mutate">
                    <TooltipWrapper
                      message={translate.t("search_findings.tab_users.add_button.tooltip")}
                    >
                      <Button id="addUser" onClick={openAddUserModal}>
                        <Glyphicon glyph="plus" />
                        &nbsp;{translate.t("search_findings.tab_users.add_button.text")}
                      </Button>
                    </TooltipWrapper>
                  </Can>
                  <Can do="backend_api_mutations_edit_stakeholder_mutate">
                    <TooltipWrapper
                      message={translate.t("search_findings.tab_users.edit_button.tooltip")}
                    >
                      <Button id="editUser" onClick={openEditUserModal} disabled={_.isEmpty(currentRow)}>
                        <FluidIcon icon="edit" />
                        &nbsp;{translate.t("search_findings.tab_users.edit_button.text")}
                      </Button>
                    </TooltipWrapper>
                  </Can>
                  <Can do="backend_api_mutations_remove_stakeholder_access_mutate">
                    <TooltipWrapper
                      message={translate.t("search_findings.tab_users.remove_user_button.tooltip")}
                    >
                      <Button
                        id="removeUser"
                        onClick={handleRemoveUser}
                        disabled={_.isEmpty(currentRow) || removing}
                      >
                        <Glyphicon glyph="minus" />
                        &nbsp;{translate.t("search_findings.tab_users.remove_user_button.text")}
                      </Button>
                    </TooltipWrapper>
                  </Can>
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
                    hideSelectColumn:
                      permissions.cannot("backend_api_mutations_edit_stakeholder_mutate")
                      || permissions.cannot("backend_api_mutations_remove_stakeholder_access_mutate"),
                    mode: "radio",
                    onSelect: setCurrentRow,
                  }}
                />
              </Col100>
            </Row>
          </Col100>
        </Row>
        <AddUserModal
          action={userModalAction}
          editTitle={translate.t("search_findings.tab_users.edit_stakeholder_title")}
          initialValues={userModalAction === "edit" ? currentRow : {}}
          onSubmit={handleSubmit}
          open={isUserModalOpen}
          onClose={closeUserModal}
          projectName={projectName}
          title={translate.t("search_findings.tab_users.title")}
          type="user"
        />
      </div>
    </React.StrictMode>
  );
};

export { projectStakeholdersView as ProjectStakeholdersView };
