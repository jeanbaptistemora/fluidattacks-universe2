import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Breadcrumb, BreadcrumbItem, Col, InputGroup, Row } from "react-bootstrap";
import { RouteComponentProps, withRouter } from "react-router";
import { Link, useHistory } from "react-router-dom";
import { EventWithDataHandler, Field } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import { stylizeBreadcrumbItem } from "../../../../utils/formatHelpers";
import { Dropdown, Text } from "../../../../utils/forms/fields";
import { useStoredState } from "../../../../utils/hooks";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { alphaNumeric } from "../../../../utils/validations";
import { GenericForm } from "../GenericForm";
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
  const handleOrganizationChange: EventWithDataHandler<React.ChangeEvent<string>> =
    (event: React.ChangeEvent<string> | undefined, organizationName: string): void => {
      setCurrentOrganization({ name: organizationName });
      push(`/organizations/${organizationName.toLowerCase()}/`);
  };

  const handleSubmit: (() => void) = (): void => undefined;

  const handleSearchSubmit: ((values: { projectName: string }) => void) = (values: { projectName: string }): void => {
    const projectName: string = values.projectName.toLowerCase();
    if (!_.isEmpty(projectName)) { push(`/groups/${projectName}/indicators`); }
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
        <Col md={9} sm={12} xs={12}>
          <Breadcrumb className={style.breadcrumb}>
          <BreadcrumbItem>
            <GenericForm
              name="organizationList"
              onSubmit={handleSubmit}>
              <Field
                component={Dropdown}
                name="organization"
                onChange={handleOrganizationChange}
                >
                {organizationList.map((organization: { name: string }, index: number) => {
                  const extraProps: Dictionary<boolean> = { selected: false };
                  if (currentOrganization.name === organization.name) {
                    extraProps.selected = true;
                  }

                  return (
                    <option value={organization.name} key={index} {...extraProps}>
                      {_.capitalize(organization.name)}
                    </option>
                  );
                })}
              </Field>
            </GenericForm>
          </BreadcrumbItem>
          {breadcrumbItems}
        </Breadcrumb>
        </Col>
        <Col md={3} sm={12} xs={12}>
          <GenericForm name="searchBar" onSubmit={handleSearchSubmit}>
            <InputGroup>
              <Field
                name="projectName"
                component={Text}
                placeholder={translate.t("navbar.searchPlaceholder")}
                validate={[alphaNumeric]}
              />
              <InputGroup.Button>
                <Button type="submit"><FluidIcon icon="search" /></Button>
              </InputGroup.Button>
            </InputGroup>
          </GenericForm>
        </Col>
      </Row>
    </React.StrictMode>
  );
};

const navbar: React.ComponentClass = withRouter(navbarComponent);

export { navbar as Navbar };
