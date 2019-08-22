import _ from "lodash";
import React from "react";
import { Breadcrumb, BreadcrumbItem, Col, InputGroup, Row } from "react-bootstrap";
import { RouteComponentProps, withRouter } from "react-router";
import { Link } from "react-router-dom";
import { Field } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import { textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { alphaNumeric } from "../../../../utils/validations";
import { GenericForm } from "../GenericForm";
import style from "./index.css";

export const navbarComponent: React.FC<RouteComponentProps> = (props: RouteComponentProps): JSX.Element => {
  const pathData: string[] = props.location.pathname.split("/")
  .splice(0 - -1);
  const handleSearchSubmit: ((values: { projectName: string }) => void) = (values: { projectName: string }): void => {
  const projectName: string = values.projectName.toUpperCase();
  if (!_.isEmpty(projectName)) { location.hash = `#!/project/${projectName}/indicators`; }
  };
  const capitalizeWord: ((wordToCapitalize: string) => string) = (wordToCapitalize: string): string =>
    translate.t(`${wordToCapitalize[0].toUpperCase()}${wordToCapitalize.slice(1)
      .toLowerCase()}`);
  const createBreadcrumbItems: ((path: string[]) => JSX.Element[]) = (path: string[]): JSX.Element[] => (
    path.map((pathDirection: string, index: number) =>
    path.slice(0, index + 1))
    .map((subPath: string[], index: number) => index > 0 ?
  (
    <BreadcrumbItem key={subPath[subPath.length - 1]}>
      <Link to={`/${subPath.join("/")}`} >
        {capitalizeWord(subPath[subPath.length - 1])}
      </Link>
    </BreadcrumbItem>
  ) : (
    <BreadcrumbItem>
    <Link to="/home">
      <b>{translate.t("navbar.breadcrumbRoot")}</b>
    </Link>
  </BreadcrumbItem>
  ))
  );

  return (
    <React.StrictMode>
      <Row className={style.container}>
        <Col md={9} sm={12} xs={12}>
          <Breadcrumb className={style.breadcrumb}>
            {createBreadcrumbItems(pathData)}
          </Breadcrumb>
        </Col>
        <Col md={3} sm={12} xs={12}>
          <GenericForm name="searchBar" onSubmit={handleSearchSubmit}>
            <InputGroup>
              <Field
                name="projectName"
                component={textField}
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

export {navbar as Navbar };
