import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Breadcrumb, BreadcrumbItem, Col, MenuItem, Row, SelectCallback, SplitButton } from "react-bootstrap";
import { RouteComponentProps, withRouter } from "react-router";
import { Link, useHistory } from "react-router-dom";
import { stylizeBreadcrumbItem } from "../../../../utils/formatHelpers";
import { useStoredState } from "../../../../utils/hooks";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { default as style } from "./index.css";
import { GET_USER_ORGANIZATIONS } from "./queries";

export const navbarComponent: React.FC<RouteComponentProps> = (props: RouteComponentProps): JSX.Element => {
  const { push } = useHistory();
  const [currentOrganization, setCurrentOrganization] = useStoredState("organization", { name: "" }, localStorage);

  const path: string = props.location.pathname;
  const pathData: string[] = path.split("/")
    .slice(2);

  // GraphQL operations
  const { data } = useQuery(GET_USER_ORGANIZATIONS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error("An error occurred fetching organizations for the navbar", error);
      });
    },
  });

  // Auxiliary Operations
  const handleOrganizationChange: ((eventKey: string, event: React.SyntheticEvent<SplitButton>) => void) =
    (eventKey: string): void => {
      if (eventKey !== currentOrganization.name) {
        setCurrentOrganization({ name: eventKey });
        push(`/organizations/${eventKey}/`);
      }
  };
  const handleOrganizationClick: (event: React.MouseEvent<SplitButton, globalThis.MouseEvent>) => void =
    () => {
      push(`/organizations/${currentOrganization.name}/`);
  };

  // Render Elements
  const organizationList: Array<{ name: string }> = _.isEmpty(data) || _.isUndefined(data)
    ? [{ name: "" }]
    : data.me.organizations.sort((a: { name: string }, b: { name: string }) => (a.name > b.name) ? 1 : -1);
  const filteredOrganizations: Array<{ name: string }> = organizationList.filter(
    (userOrganization: { name: string }) => path.includes(userOrganization.name),
  );
  const filteredOrganization: string = filteredOrganizations.length === 0
    ? organizationList[0].name
    : filteredOrganizations[0].name;

  const setOrganization: () => void = (): void => {
    if (!_.isEmpty(filteredOrganization)) {
      setCurrentOrganization({ name: filteredOrganization });
    }
  };

  React.useEffect(setOrganization, [filteredOrganization]);

  const breadcrumbItems: JSX.Element[] = pathData.slice(1)
    .map((item: string, index: number) => {
      const baseLink: string = path.split("/")[1];
      const link: string = pathData.slice(0, index + 2)
        .join("/");

      return (
        <BreadcrumbItem key={index}>
          <Link to={`/${baseLink}/${link}`}>{stylizeBreadcrumbItem(item)}</Link>
        </BreadcrumbItem>
      );
    });

  return (
    <React.StrictMode>
      <Row id="navbar" className={style.container}>
        <Col md={12} sm={12} xs={12}>
          <Breadcrumb className={style.breadcrumb}>
          <BreadcrumbItem>
          <div className={style.splitButton}>
            <SplitButton
              id={"organizationList"}
              onClick={handleOrganizationClick}
              onSelect={handleOrganizationChange as SelectCallback}
              title={currentOrganization.name}
            >
              {organizationList.map((organization: {name: string}) =>
                <MenuItem
                  eventKey={organization.name}
                  key={organization.name}
                >
                  {organization.name}
                </MenuItem>,
              )}
            </SplitButton>
          </div>
          </BreadcrumbItem>
          {breadcrumbItems}
        </Breadcrumb>
        </Col>
      </Row>
    </React.StrictMode>
  );
};

const navbar: React.ComponentClass = withRouter(navbarComponent);

export { navbar as Navbar };
