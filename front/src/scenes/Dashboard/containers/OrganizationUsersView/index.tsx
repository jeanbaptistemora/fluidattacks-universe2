import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { useParams } from "react-router";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { FluidIcon } from "../../../../components/FluidIcon/index";
import { TooltipWrapper } from "../../../../components/TooltipWrapper/index";
import { formatUserlist } from "../../../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { GET_ORGANIZATION_ID } from "../OrganizationPoliciesView/queries";
import { GET_ORGANIZATION_USERS } from "./queries";
import { IUserAttrs } from "./types";

const organizationUsers: React.FC = (): JSX.Element => {
  const { organizationName } = useParams<{ organizationName: string }>();

  // State management
  const [currentRow, setCurrentRow] = React.useState<Dictionary<string>>({});

  // GraphQL Operations
  const { data: basicData } = useQuery(GET_ORGANIZATION_ID, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error("An error occurred fetching organization ID", error);
      });
    },
    variables: {
      organizationName: organizationName.toLowerCase(),
    },
  });

  const { data } = useQuery(GET_ORGANIZATION_USERS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error(
          "An error occurred fetching organization users",
          error,
        );
      });
    },
    skip: !basicData,
    variables: {
      organizationId: basicData && basicData.organizationId.id,
    },
  });

  // Auxiliary elements
  const tableHeaders: IHeader[] = [
    {
      dataField: "email",
      header: translate.t("search_findings.users_table.usermail"),
      width: "27%",
    },
    {
      dataField: "phoneNumber",
      header: translate.t("search_findings.users_table.phoneNumber"),
      width: "13%",
    },
    {
      dataField: "organization",
      header: translate.t("search_findings.users_table.userOrganization"),
      width: "12%",
    },
    {
      dataField: "firstLogin",
      header: translate.t("search_findings.users_table.firstlogin"),
      width: "12%",
    },
    {
      dataField: "lastLogin",
      header: translate.t("search_findings.users_table.lastlogin"),
      width: "12%",
    },
  ];

  // Render Elements
  const userList: IUserAttrs[] = _.isUndefined(data) || _.isEmpty(data)
    ? []
    : formatUserlist(data.organization.users);

  return (
    <React.StrictMode>
      <div id="users" className="tab-pane cont active" >
        <Row>
          <Col md={12} sm={12} xs={12}>
            <Row>
              <Col md={12} sm={12}>
                <DataTableNext
                  id="tblUsers"
                  bordered={true}
                  dataset={userList}
                  exportCsv={true}
                  headers={tableHeaders}
                  pageSize={15}
                  remote={false}
                  search={true}
                  striped={true}
                  title=""
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
      </div>
    </React.StrictMode>
    );
};

export { organizationUsers as OrganizationUsers };
