import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import {
  Breadcrumb,
  BreadcrumbItem,
  InputGroup,
  MenuItem,
  Nav,
  Navbar,
  NavItem,
  SelectCallback,
  SplitButton,
} from "react-bootstrap";
import { RouteComponentProps, withRouter } from "react-router";
import { Link, useHistory } from "react-router-dom";
import { Field } from "redux-form";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { default as style } from "scenes/Dashboard/components/Navbar/index.css";
import { GET_USER_ORGANIZATIONS } from "scenes/Dashboard/components/Navbar/queries";
import { stylizeBreadcrumbItem } from "scenes/Dashboard/components/Navbar/utils";
import { NewsWidget } from "scenes/Dashboard/components/NewsWidget";
import { Text } from "utils/forms/fields";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { alphaNumeric } from "utils/validations";

export const navbarComponent: React.FC<RouteComponentProps> = (
  props: RouteComponentProps,
): JSX.Element => {
  const { push } = useHistory();
  const [lastOrganization, setLastOrganization] = useStoredState(
    "organization",
    { name: "" },
    localStorage,
  );
  const { userEmail } = window as typeof window & { userEmail: string };

  const path: string = props.location.pathname;
  const pathData: string[] = path.split("/")
    .slice(2);
  const pathOrganization: string = path.includes("/orgs")
    ? pathData[0].toLowerCase()
    : lastOrganization.name;

  // GraphQL operations
  const { data, refetch: refetchOrganizationList } = useQuery(
    GET_USER_ORGANIZATIONS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(translate.t("group_alerts.error_textsad"));
          Logger.warning(
            "An error occurred fetching organizations for the navbar",
            error,
          );
        });
      },
    },
  );

  // Auxiliary Operations
  const handleOrganizationChange: (
    eventKey: string,
    event: React.SyntheticEvent<SplitButton>,
  ) => void = (eventKey: string): void => {
    if (eventKey !== lastOrganization.name) {
      setLastOrganization({ name: eventKey });
      push(`/orgs/${eventKey}/`);
    }
  };
  const handleOrganizationClick: (
    event: React.MouseEvent<SplitButton, globalThis.MouseEvent>,
  ) => void = () => {
    push(`/orgs/${lastOrganization.name}/`);
  };
  const handleSearchSubmit: (values: {
    projectName: string;
  }) => void = (values: { projectName: string }): void => {
    const projectName: string = values.projectName.toLowerCase();
    if (!_.isEmpty(projectName)) {
      push(`/groups/${projectName}/indicators`);
    }
  };

  // Render Elements
  const organizationList: Array<{ name: string }> =
    _.isEmpty(data) || _.isUndefined(data)
      ? [{ name: "" }]
      : data.me.organizations.sort((a: { name: string }, b: { name: string }) =>
          a.name > b.name ? 1 : -1,
        );

  React.useEffect((): void => {
    refetchOrganizationList();
    setLastOrganization({ name: pathOrganization });
  },              [pathOrganization]);

  const breadcrumbItems: JSX.Element[] = pathData
    .slice(1)
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
      <Navbar className={style.container} fluid={true} id={"navbar"}>
        <Navbar.Header>
          <Breadcrumb className={style.breadcrumb}>
            <BreadcrumbItem>
              <div className={style.splitButton}>
                <SplitButton
                  id={"organizationList"}
                  onClick={handleOrganizationClick}
                  onSelect={handleOrganizationChange as SelectCallback}
                  title={pathOrganization}
                >
                  {organizationList.map((organization: { name: string }) => (
                    <MenuItem
                      eventKey={organization.name}
                      key={organization.name}
                    >
                      {organization.name}
                    </MenuItem>
                  ))}
                </SplitButton>
              </div>
            </BreadcrumbItem>
            {breadcrumbItems}
          </Breadcrumb>
          <Navbar.Toggle />
        </Navbar.Header>
        <Navbar.Collapse>
          <Nav pullRight={true}>
            <NavItem>
              <NewsWidget />
            </NavItem>
            {userEmail.endsWith("fluidattacks.com") ? (
              <li role="presentation">
                <Navbar.Form style={{ marginBottom: "4px", marginTop: "4px" }}>
                  <GenericForm name={"searchBar"} onSubmit={handleSearchSubmit}>
                    <InputGroup className={style.groupsInput}>
                      <Field
                        component={Text}
                        name={"projectName"}
                        placeholder={translate.t("navbar.searchPlaceholder")}
                        validate={[alphaNumeric]}
                      />
                      <InputGroup.Button>
                        <Button className={style.searchButton} type={"submit"}>
                          <FluidIcon icon={"search"} />
                        </Button>
                      </InputGroup.Button>
                    </InputGroup>
                  </GenericForm>
                </Navbar.Form>
              </li>
            ) : undefined}
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    </React.StrictMode>
  );
};

const navbar: React.ComponentClass = withRouter(navbarComponent);

export { navbar as Navbar };
