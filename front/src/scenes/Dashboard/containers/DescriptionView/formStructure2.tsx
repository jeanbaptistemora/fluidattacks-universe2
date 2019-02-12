import _ from "lodash";
import React from "react";
import { Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import globalStyle from "../../../../styles/global.css";
import { formatCweUrl, formatDropdownField } from "../../../../utils/formatHelpers";
import { dropdownField, textAreaField, textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { numberBetween, numeric, required } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { IDescriptionViewProps } from "./index";

type renderFormFieldsFn = ((props: IDescriptionViewProps) => JSX.Element);

const severityBetween: ((value: number) => string | undefined) = numberBetween(0, 5);

const calcRiskLevel: ((probability: string, severity: number) => string) =
  (probability: string, severity: number): string => {
    const probabilityValue: number = Number(probability
      .substring(0, 3)
      .replace("%", ""));

    return ((probabilityValue / 100) * severity).toFixed(1);
  };

const renderDetailedFields: renderFormFieldsFn = (props: IDescriptionViewProps): JSX.Element => (
  <React.Fragment>
    <Row>
      <Col md={6} sm={12} xs={12}>
        <EditableField
          component={textField}
          currentValue={props.dataset.clientCode}
          label={translate.t("search_findings.tab_description.customer_project_code")}
          name="clientCode"
          renderAsEditable={props.isEditing}
          type="text"
          validate={[required]}
        />
      </Col>
      <Col md={6} sm={12} xs={12}>
        <EditableField
          component={textField}
          currentValue={props.dataset.clientProject}
          label={translate.t("search_findings.tab_description.customer_project_name")}
          name="clientProject"
          renderAsEditable={props.isEditing}
          type="text"
          validate={[required]}
        />
      </Col>
    </Row>
    <Row>
      <Col md={4} sm={12} xs={12}>
        <EditableField
          component={dropdownField}
          currentValue={props.dataset.clientCode}
          label={translate.t("search_findings.tab_description.probability.title")}
          name="probability"
          renderAsEditable={props.isEditing}
          validate={[required]}
        >
          <option value="" selected={true} />
          <option value="100% Vulnerado Anteriormente">
            {translate.t("search_findings.tab_description.probability.100")}
          </option>
          <option value="75% Fácil de vulnerar">{translate.t("search_findings.tab_description.probability.75")}</option>
          <option value="50% Posible de vulnerar">
            {translate.t("search_findings.tab_description.probability.50")}
          </option>
          <option value="25% Difícil de vulnerar">
            {translate.t("search_findings.tab_description.probability.25")}
          </option>
        </EditableField>
      </Col>
      <Col md={4} sm={12} xs={12}>
        <EditableField
          component={textField}
          currentValue={props.dataset.probability}
          label={translate.t("search_findings.tab_description.severity")}
          name="detailedSeverity"
          renderAsEditable={props.isEditing}
          type="number"
          validate={[required, severityBetween]}
        />
      </Col>
      <Col md={4} sm={12} xs={12}>
        <EditableField
          component={textField}
          currentValue={calcRiskLevel(props.formValues.probability, props.formValues.detailedSeverity)}
          label={translate.t("search_findings.tab_description.risk_level")}
          name="riskLevel"
          renderAsEditable={false}
          type="text"
        />
      </Col>
    </Row>
    <Row>
      <Col md={6} sm={12} xs={12}>
        <EditableField
          component={dropdownField}
          currentValue={translate.t(formatDropdownField(props.dataset.ambit))}
          label={translate.t("search_findings.tab_description.ambit.title")}
          name="ambit"
          renderAsEditable={props.isEditing}
          validate={[required]}
        >
          <option value="" selected={true} />
          <option value="APPLICATIONS">{translate.t("search_findings.tab_description.ambit.applications")}</option>
          <option value="DATABASES">{translate.t("search_findings.tab_description.ambit.databases")}</option>
          <option value="SOURCE_CODE">{translate.t("search_findings.tab_description.ambit.sourcecode")}</option>
          <option value="INFRASTRUCTURE">{translate.t("search_findings.tab_description.ambit.infra")}</option>
        </EditableField>
      </Col>
      <Col md={6} sm={12} xs={12}>
        <EditableField
          component={dropdownField}
          currentValue={props.dataset.category}
          label={translate.t("search_findings.tab_description.category.title")}
          name="category"
          renderAsEditable={props.isEditing}
          validate={[required]}
        >
          <option value="" selected={true} />
          <option value="Actualizar y configurar las líneas base de seguridad de los componentes">
            {translate.t("search_findings.tab_description.category.update_sec_baselines")}
          </option>
          <option value="Definir el modelo de autorización considerando el principio de mínimo privilegio">
            {translate.t("search_findings.tab_description.category.define_auth_model")}
          </option>
          <option value="Desempeño">{translate.t("search_findings.tab_description.category.performance")}</option>
          <option value="Eventualidad">{translate.t("search_findings.tab_description.category.event")}</option>
          <option value="Evitar exponer la información técnica de la aplicación, servidores y plataformas">
            {translate.t("search_findings.tab_description.category.expose_tech_info")}
          </option>
          <option value="Excluir datos sensibles del código fuente y del registro de eventos">
            {translate.t("search_findings.tab_description.category.sensible_data_code")}
          </option>
          <option value="Fortalecer controles en autenticación y manejo de sesión">
            {translate.t("search_findings.tab_description.category.strengthen_auth_session")}
          </option>
          <option value="Fortalecer controles en el procesamiento de archivos">
            {translate.t("search_findings.tab_description.category.strengthen_file_processing")}
          </option>
          <option
            value="Fortalecer la protección de datos almacenados relacionados con contraseñas o llaves criptográficas"
          >
            {translate.t("search_findings.tab_description.category.strengthen_password_keys")}
          </option>
          <option value="Implementar controles para validar datos de entrada">
            {translate.t("search_findings.tab_description.category.validate_input")}
          </option>
          <option value="Mantenibilidad">
            {translate.t("search_findings.tab_description.category.maintainability")}
          </option>
          <option value="Registrar eventos para trazabilidad y auditoría">
            {translate.t("search_findings.tab_description.category.log_events")}
          </option>
          <option value="Utilizar protocolos de comunicación seguros">
            {translate.t("search_findings.tab_description.category.secure_protocols")}
          </option>
          <option value="Validar la integridad de las transacciones en peticiones HTTP">
            {translate.t("search_findings.tab_description.category.http_req_integrity")}
          </option>
        </EditableField>
      </Col>
    </Row>
  </React.Fragment>
);

const renderDescriptionFields: renderFormFieldsFn = (props: IDescriptionViewProps): JSX.Element => {
  const isDetailed: boolean = props.formValues.reportLevel === "DETAILED";

  return (
    <React.Fragment>
      {isDetailed && props.isEditing ? renderDetailedFields(props) : undefined}
    </React.Fragment>
  );
};

export const renderFormFields: renderFormFieldsFn = (props: IDescriptionViewProps): JSX.Element => {
  const canEditDescription: boolean = _.includes(["admin", "analyst"], props.userRole);
  const canEditTreatment: boolean = _.includes(["customer", "customeradmin"], props.userRole);

  return (
    <React.Fragment>
      {!props.isEditing || (props.isEditing && canEditDescription) ? renderDescriptionFields(props) : undefined}
    </React.Fragment>
  );
};
