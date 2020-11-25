import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import {
  InputGroup,
  MenuItem,
  Navbar,
  SelectCallback,
  SplitButton,
} from "react-bootstrap";
import { withRouter } from "react-router";
import { Link, useHistory, useLocation } from "react-router-dom";
import { Field } from "redux-form";
import {
  BreadCrumb,
  Col100,
  Col25,
  NavBar,
  NavBarCollapse,
  NavBarHeader,
} from "styles/styledComponents";

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

export const navbarComponent: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const { pathname } = useLocation();
  const [lastOrganization, setLastOrganization] = useStoredState(
    "organization",
    { name: "" },
    localStorage,
  );
  const { userEmail } = window as typeof window & { userEmail: string };

  const path: string = pathname;
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
        <li key={index}>
          <Link to={`/${baseLink}/${link}`}>{stylizeBreadcrumbItem(item)}</Link>
        </li>
      );
    });

  return (
    <React.StrictMode>
      <NavBar id={"navbar"}>
        <NavBarHeader>
          <BreadCrumb>
            <li>
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
            </li>
            {breadcrumbItems}
          </BreadCrumb>
        </NavBarHeader>
        <NavBarCollapse>
          <Col25>
            <NewsWidget />
          </Col25>
          <Col100>
            {userEmail.endsWith("fluidattacks.com") ? (
              <li role="presentation">
                <Navbar.Form className={style.navbarForm}>
                  <GenericForm name={"searchBar"} onSubmit={handleSearchSubmit}>
                    <InputGroup className={style.groupsInput}>
                      <Field
                        component={Text}
                        name={"projectName"}
                        placeholder={translate.t("navbar.searchPlaceholder")}
                        validate={[alphaNumeric]}
                      />
                      <InputGroup.Button>
                        <Button className={"bg-sb b--sb"} type={"submit"}>
                          <FluidIcon icon={"search"} />
                        </Button>
                      </InputGroup.Button>
                    </InputGroup>
                  </GenericForm>
                </Navbar.Form>
              </li>
            ) : undefined}
          </Col100>
        </NavBarCollapse>
      </NavBar>
    </React.StrictMode>
  );
};

const navbar: React.ComponentClass = withRouter(navbarComponent);

export { navbar as Navbar };
