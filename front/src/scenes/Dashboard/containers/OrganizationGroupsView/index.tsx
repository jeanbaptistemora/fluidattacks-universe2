import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import {
  ButtonToolbar, Col, Glyphicon, Row, ToggleButton, ToggleButtonGroup,
} from "react-bootstrap";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeaderConfig } from "../../../../components/DataTableNext/types";
import { useStoredState } from "../../../../utils/hooks";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { ProjectBox } from "../../components/ProjectBox";
import { default as style } from "../HomeView/index.css";
import { GET_ORGANIZATION_GROUPS } from "./queries";
import { IOrganizationGroups, IOrganizationGroupsProps } from "./types";

const tableHeaders: IHeaderConfig[] = [
  { dataField: "name", header: "Group Name" },
  { dataField: "description", header: "Description" },
];

const organizationGroups: React.FC<IOrganizationGroupsProps> = (props: IOrganizationGroupsProps): JSX.Element => {
  const { organizationId } = props;

  // State management
  const [display, setDisplay] = useStoredState("groupsDisplay", { mode: "grid" });
  const handleDisplayChange: ((value: string) => void) = (value: string): void => {
    setDisplay({ mode: value });
  };

  // GraphQL operations
  const { data } = useQuery(GET_ORGANIZATION_GROUPS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error("An error occurred loading organization groups", error);
      });
    },
    variables: {
      organizationId,
    },
  });

  const goToGroup: ((groupName: string) => void) = (groupName: string): void => undefined;

  return (
    <React.StrictMode>
      <div className={style.container}>
        <Row>
          <Col sm={12}>
            <ButtonToolbar className={style.displayOptions}>
              <ToggleButtonGroup
                defaultValue="grid"
                name="displayOptions"
                onChange={handleDisplayChange}
                type="radio"
                value={display.mode}
              >
                <ToggleButton value="grid"><Glyphicon glyph="th" /></ToggleButton>
                <ToggleButton value="list"><Glyphicon glyph="th-list" /></ToggleButton>
              </ToggleButtonGroup>
            </ButtonToolbar>
          </Col>
        </Row>
        {(_.isUndefined(data) || _.isEmpty(data)) ? <React.Fragment /> : (
          <React.Fragment>
            <Row>
              <Col md={12}>
                <Row className={style.content}>
                  {display.mode === "grid"
                    ? data.organization.projects.map(
                        (group: IOrganizationGroups["data"]["organization"]["projects"][0], index: number):
                        JSX.Element => (
                          <Col md={3} key={index}>
                            <ProjectBox
                              name={group.name.toUpperCase()}
                              description={group.description}
                              onClick={goToGroup}
                            />
                          </Col>
                      ))
                    : (
                      <DataTableNext
                        bordered={true}
                        dataset={data.organization.projects}
                        exportCsv={false}
                        headers={tableHeaders}
                        id="tblGroups"
                        pageSize={15}
                        search={true}
                      />
                    )
                  }
                </Row>
              </Col>
            </Row>
          </React.Fragment>
        )}
      </div>
    </React.StrictMode>
  );
};

export { organizationGroups as OrganizationGroups };
