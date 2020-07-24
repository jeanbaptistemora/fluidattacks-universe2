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
  const [currentOrganization, setCurrentOrganization] = useStoredState("organization", { name: "" });

  const path: string = props.location.pathname;
  const renderOrganizationBox: boolean = path.includes("organizations");
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
  if (_.isEmpty(data) || _.isUndefined(data)) {
    return <React.Fragment />;
  }

  const filteredOrganization: Array<{ name: string }> = data.me.organizations.filter(
    (userOrganization: { name: string }) => path.includes(userOrganization.name),
  );

  if (renderOrganizationBox && !path.includes(currentOrganization.name)) {
    setCurrentOrganization({ name: filteredOrganization[0].name });
  }

  const breadcrumbItems: JSX.Element[] = pathData.map((item: string, index: number) => {
    const baseLink: string = path.split("/")[1];
    const link: string = pathData.slice(0, index + 1)
      .join("/");

    return (
      <BreadcrumbItem key={index}>
        <Link to={`/${baseLink}/${link}`}>{_.capitalize(item)}</Link>
      </BreadcrumbItem>
    );
  });

  return (
    <React.StrictMode>
      <Row id="navbar" className={style.container}>
        <Col md={renderOrganizationBox ? 6 : 9} sm={12} xs={12}>
          <Breadcrumb className={style.breadcrumb}>
            <BreadcrumbItem>
              <Link to="/home"><b>{translate.t("navbar.breadcrumbRoot")}</b></Link>
            </BreadcrumbItem>
            {breadcrumbItems}
          </Breadcrumb>
        </Col>
        {renderOrganizationBox
          ? (
            <React.Fragment>
              <Col md={3} sm={12} xs={12}>
                <GenericForm
                  initialValues={{
                    organization: currentOrganization.name,
                  }}
                  name="organizationList"
                  onSubmit={handleSubmit}>
                  <div className={style.organizationForm}>
                    <Field
                      component={Dropdown}
                      name="organization"
                      onChange={handleOrganizationChange}
                    >
                      {data.me.organizations.map((organization: { name: string }, index: number) => (
                        <option value={organization.name} key={index}>
                          {organization.name.toUpperCase()}
                        </option>
                      ))}
                    </Field>
                  </div>
                </GenericForm>
              </Col>
            </React.Fragment>
          )
          : undefined
        }
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
