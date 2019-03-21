import _ from "lodash";
import React from "react";
import { Breadcrumb, BreadcrumbItem, Button, Col, Glyphicon, InputGroup, Row } from "react-bootstrap";
import { RouteComponentProps, withRouter } from "react-router";
import { Link } from "react-router-dom";
import { Field } from "redux-form";
import { textField } from "../../../../utils/forms/fields";
import { GenericForm } from "../GenericForm";
import style from "./index.css";

const navbar: React.SFC<RouteComponentProps> = (props: RouteComponentProps): JSX.Element => {
  const pathData: string[] = props.location.pathname.split("/");
  const currentProject: string = pathData.length > 2 ? pathData[2].toUpperCase() : "";
  const handleSearchSubmit: ((values: { projectName: string }) => void) = (values: { projectName: string }): void => {
    const projectName: string = values.projectName.toUpperCase();

    if (!_.isEmpty(projectName)) { props.history.push({ pathname: `/project/${projectName}/indicators` }); }
  };

  return (
    <React.StrictMode>
      <Row className={style.container}>
        <Col md={9} sm={12} xs={12}>
          <Breadcrumb className={style.breadcrumb}>
            <BreadcrumbItem><Link to="/home"><b>My Projects</b></Link></BreadcrumbItem>
            <BreadcrumbItem><Link to={`/project/${currentProject}/indicators`}>{currentProject}</Link></BreadcrumbItem>
          </Breadcrumb>
        </Col>
        <Col md={3} sm={12} xs={12}>
          <GenericForm name="searchBar" onSubmit={handleSearchSubmit}>
            <InputGroup>
              <Field name="projectName" component={textField} placeholder="Project Name" />
              <InputGroup.Button>
                <Button type="submit"><Glyphicon glyph="search" /></Button>
              </InputGroup.Button>
            </InputGroup>
          </GenericForm>
        </Col>
      </Row>
    </React.StrictMode>
  );
};

export = withRouter(navbar);
