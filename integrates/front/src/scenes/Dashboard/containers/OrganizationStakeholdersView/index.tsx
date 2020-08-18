import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { useParams } from "react-router";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeaderConfig } from "../../../../components/DataTableNext/types";
import { FluidIcon } from "../../../../components/FluidIcon/index";
import { TooltipWrapper } from "../../../../components/TooltipWrapper/index";
import { formatLastLogin, formatUserlist } from "../../../../utils/formatHelpers";
import { Logger } from "../../../../utils/logger";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import { sortLastLogin } from "../../../../utils/sortHelpers";
import translate from "../../../../utils/translations/translate";
import { addUserModal as AddUserModal } from "../../components/AddUserModal/index";
import {
  ADD_STAKEHOLDER_MUTATION,
  EDIT_STAKEHOLDER_MUTATION,
  GET_ORGANIZATION_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
} from "./queries";
import {
  IAddStakeholderAttrs,
  IEditStakeholderAttrs,
  IOrganizationStakeholders,
  IRemoveStakeholderAttrs,
  IStakeholderAttrs,
} from "./types";

const tableHeaders: IHeaderConfig[] = [
  {
    dataField: "email",
    header: translate.t("search_findings.users_table.usermail"),
    width: "27%",
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
    dataField: "phoneNumber",
    header: translate.t("search_findings.users_table.phoneNumber"),
    width: "13%",
  },
  {
    dataField: "firstLogin",
    header: translate.t("search_findings.users_table.firstlogin"),
    width: "12%",
  },
  {
    dataField: "lastLogin",
    formatter: formatLastLogin,
    header: translate.t("search_findings.users_table.lastlogin"),
    sortFunc: sortLastLogin,
    width: "12%",
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
  const { userName } = window as typeof window & Dictionary<string>;

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
  const { data, refetch: refetchStakeholders } = useQuery(GET_ORGANIZATION_STAKEHOLDERS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning(
          "An error occurred fetching organization stakeholders",
          error,
        );
      });
    },
    variables: { organizationId },
  });

  const [grantStakeholderAccess] = useMutation(ADD_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IAddStakeholderAttrs): void => {
      if (mtResult.grantStakeholderOrganizationAccess.success) {
        refetchStakeholders()
          .catch();
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
        refetchStakeholders()
          .catch();
        mixpanel.track("EditUserOrganizationAccess", { Organization: organizationName, User: userName });
        const { email } = mtResult.editStakeholderOrganization.modifiedStakeholder;
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
      if (mtResult.removeStakeholderOrganizationAccess.success) {
        refetchStakeholders()
          .catch();
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
      grantStakeholderAccess({ variables: {
        ...values,
        organizationId,
      } })
        .catch();
    } else {
      editStakeholder({ variables: {
        ...values,
        organizationId,
      } })
        .catch();
    }
  };

  const handleRemoveStakeholder: (() => void) = (): void => {
    removeStakeholderAccess({ variables: {
      organizationId,
      userEmail: currentRow.email,
    } })
      .catch();
    setStakeholderModalAction("add");
  };

  // Render Elements
  const stakeholdersList: IStakeholderAttrs[] = _.isUndefined(data) || _.isEmpty(data)
    ? []
    : formatUserlist(data.organization.stakeholders);

  return (
    <React.StrictMode>
      <div id="users" className="tab-pane cont active" >
        <Row>
          <Col md={12} sm={12} xs={12}>
            <Row>
              <Col md={12} sm={12}>
                <ButtonToolbar className="pull-right md-12 sm-12">
                    <TooltipWrapper
                      message={translate.t("organization.tabs.users.addButton.tooltip")}
                    >
                      <Button id="addUser" onClick={openAddStakeholderModal}>
                        <Glyphicon glyph="plus" />
                        &nbsp;{translate.t("organization.tabs.users.addButton.text")}
                      </Button>
                    </TooltipWrapper>
                    <TooltipWrapper
                      message={translate.t("organization.tabs.users.editButton.tooltip")}
                    >
                      <Button id="editUser" onClick={openEditStakeholderModal} disabled={_.isEmpty(currentRow)}>
                        <FluidIcon icon="edit" />
                        &nbsp;{translate.t("organization.tabs.users.editButton.text")}
                      </Button>
                    </TooltipWrapper>
                    <TooltipWrapper
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
              </Col>
            </Row>
            <br />
            <Row>
              <Col md={12} sm={12}>
                <DataTableNext
                  id="tblUsers"
                  bordered={true}
                  dataset={stakeholdersList}
                  exportCsv={true}
                  headers={tableHeaders}
                  pageSize={15}
                  search={true}
                  striped={true}
                  selectionMode={{
                    clickToSelect: true,
                    mode: "radio",
                    onSelect: setCurrentRow,
                  }}
                />
              </Col>
            </Row>
          </Col>
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
