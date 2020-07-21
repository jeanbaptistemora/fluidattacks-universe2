import _ from "lodash";
import React from "react";
import { Breadcrumb, BreadcrumbItem, Col, InputGroup, Row } from "react-bootstrap";
import { RouteComponentProps, withRouter } from "react-router";
import { Link, useHistory } from "react-router-dom";
import { Field } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import { Text } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { alphaNumeric } from "../../../../utils/validations";
import { GenericForm } from "../GenericForm";
import { default as style } from "./index.css";

export const navbarComponent: React.FC<RouteComponentProps> = (props: RouteComponentProps): JSX.Element => {
  const { push } = useHistory();
  const handleSearchSubmit: ((values: { projectName: string }) => void) = (values: { projectName: string }): void => {
    const projectName: string = values.projectName.toLowerCase();
    if (!_.isEmpty(projectName)) { push(`/groups/${projectName}/indicators`); }
  };

  const pathData: string[] = props.location.pathname.split("/")
    .slice(2);
  const breadcrumbItems: JSX.Element[] = pathData.map((item: string, index: number) => {
    const baseLink: string = props.location.pathname.split("/")[1];
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
        <Col md={9} sm={12} xs={12}>
          <Breadcrumb className={style.breadcrumb}>
            <BreadcrumbItem>
              <Link to="/home"><b>{translate.t("navbar.breadcrumbRoot")}</b></Link>
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
