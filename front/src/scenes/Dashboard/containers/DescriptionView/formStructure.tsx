import _ from "lodash";
import React from "react";
import { Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import globalStyle from "../../../../styles/global.css";
import {
  formatCweUrl,
  formatDropdownField,
  formatFindingType,
} from "../../../../utils/formatHelpers";
import { dropdownField, textAreaField, textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { numberBetween, numeric, required } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { TreatmentFieldsView } from "../../components/treatmentFields";
import { VulnerabilitiesView } from "../../components/Vulnerabilities";
import { IDescriptionViewProps } from "./index";

type renderFormFieldsFn = ((props: IDescriptionViewProps) => JSX.Element);

const severityBetween: ((value: number) => string | undefined) = numberBetween(0, 5);

const calcRiskLevel: ((probability: number, severity: number) => string) =
  (probability: number, severity: number): string =>

    ((probability / 100) * severity).toFixed(1);

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
          currentValue={props.dataset.probability}
          label={translate.t("search_findings.tab_description.probability.title")}
          name="probability"
          renderAsEditable={props.isEditing}
          type="number"
          validate={[required]}
        >
          <option value="" selected={true} />
          <option value="100">
            {translate.t("search_findings.tab_description.probability.100")}
          </option>
          <option value="75">{translate.t("search_findings.tab_description.probability.75")}</option>
          <option value="50">
            {translate.t("search_findings.tab_description.probability.50")}
          </option>
          <option value="25">
            {translate.t("search_findings.tab_description.probability.25")}
          </option>
        </EditableField>
      </Col>
      <Col md={4} sm={12} xs={12}>
        <EditableField
          component={textField}
          currentValue={props.dataset.detailedSeverity}
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

  const canEditDescription: boolean =
  (props.isEditing && _.includes(["admin", "analyst"], props.userRole));

  const canRenderDetailedField: boolean =
  isDetailed && props.isEditing && !_.includes(["customer", "customeradmin"], props.userRole);

  const validateEmptyField: boolean = !props.isEditing || canEditDescription;

  return (
    <React.Fragment>
      <Row>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            component={dropdownField}
            currentValue={formatFindingType(props.dataset.type)}
            label={translate.t("search_findings.tab_description.type.title")}
            name="type"
            renderAsEditable={props.isEditing}
            validate={[required]}
            visible={validateEmptyField}
          >
            <option value="" selected={true} />
            <option value="SECURITY">{translate.t("search_findings.tab_description.type.security")}</option>
            <option value="HYGIENE">{translate.t("search_findings.tab_description.type.hygiene")}</option>
          </EditableField>
        </Col>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            component={textField}
            currentValue={props.dataset.analyst}
            label={translate.t("search_findings.tab_description.analyst")}
            name="analyst"
            renderAsEditable={false}
            validate={[required]}
            visible={!props.isEditing && _.includes(["analyst", "admin"], props.userRole)}
          />
        </Col>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            component={dropdownField}
            currentValue={props.dataset.reportLevel}
            label={translate.t("search_findings.tab_description.reportLevel.title")}
            name="reportLevel"
            renderAsEditable={props.isEditing}
            validate={[required]}
            visible={props.isEditing && _.includes(["admin", "analyst"], props.userRole)}
          >
            <option value="" selected={true} />
            <option value="DETAILED">{translate.t("search_findings.tab_description.reportLevel.detailed")}</option>
            <option value="GENERAL">{translate.t("search_findings.tab_description.reportLevel.general")}</option>
          </EditableField>
        </Col>
      </Row>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <EditableField
            component={textField}
            currentValue={props.dataset.title}
            label={translate.t("search_findings.tab_description.title")}
            name="title"
            renderAsEditable={props.isEditing}
            type="text"
            validate={[required]}
            visible={props.isEditing && _.includes(["admin", "analyst"], props.userRole)}
          />
        </Col>
      </Row>
        {canRenderDetailedField ? renderDetailedFields(props) : undefined}
      <Row>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            component={dropdownField}
            currentValue={translate.t(formatDropdownField(props.dataset.scenario))}
            label={translate.t("search_findings.tab_description.scenario.title")}
            name="scenario"
            renderAsEditable={props.isEditing}
            validate={[required]}
            visible={validateEmptyField}
          >
            <option value="" selected={true} />
            <option value="ANONYMOUS_INTERNET">
              {translate.t("search_findings.tab_description.scenario.anon_inter")}
            </option>
            <option value="ANONYMOUS_INTRANET">
              {translate.t("search_findings.tab_description.scenario.anon_intra")}
            </option>
            <option value="AUTHORIZED_USER_EXTRANET">
              {translate.t("search_findings.tab_description.scenario.auth_extra")}
            </option>
            <option value="UNAUTHORIZED_USER_EXTRANET">
              {translate.t("search_findings.tab_description.scenario.unauth_extra")}
            </option>
            <option value="AUTHORIZED_USER_INTERNET">
              {translate.t("search_findings.tab_description.scenario.auth_inter")}
            </option>
            <option value="UNAUTHORIZED_USER_INTERNET">
              {translate.t("search_findings.tab_description.scenario.unauth_inter")}
            </option>
            <option value="AUTHORIZED_USER_INTRANET">
              {translate.t("search_findings.tab_description.scenario.auth_intra")}
            </option>
            <option value="UNAUTHORIZED_USER_INTRANET">
              {translate.t("search_findings.tab_description.scenario.unauth_intra")}
            </option>
          </EditableField>
        </Col>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            component={dropdownField}
            currentValue={translate.t(formatDropdownField(props.dataset.actor))}
            label={translate.t("search_findings.tab_description.actor.title")}
            name="actor"
            renderAsEditable={props.isEditing}
            validate={[required]}
            visible={validateEmptyField}
          >
            <option value="" selected={true} />
            <option value="ANYONE_INTERNET">{translate.t("search_findings.tab_description.actor.any_internet")}</option>
            <option value="ANY_CUSTOMER">{translate.t("search_findings.tab_description.actor.any_customer")}</option>
            <option value="SOME_CUSTOMERS">{translate.t("search_findings.tab_description.actor.some_customer")}</option>
            <option value="ANYONE_WORKSTATION">
              {translate.t("search_findings.tab_description.actor.any_station")}
            </option>
            <option value="ANY_EMPLOYEE">{translate.t("search_findings.tab_description.actor.any_employee")}</option>
            <option value="SOME_EMPLOYEES">{translate.t("search_findings.tab_description.actor.some_employee")}</option>
            <option value="ONE_EMPLOYEE">{translate.t("search_findings.tab_description.actor.one_employee")}</option>
          </EditableField>
        </Col>
      </Row>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <EditableField
            className={globalStyle.noResize}
            component={textAreaField}
            currentValue={props.dataset.description}
            label={translate.t("search_findings.tab_description.description")}
            name="description"
            renderAsEditable={props.isEditing}
            type="text"
            validate={[required]}
            visible={validateEmptyField}
          />
        </Col>
        <Col md={12} sm={12} xs={12}>
          <EditableField
            className={globalStyle.noResize}
            component={textAreaField}
            currentValue={props.dataset.requirements}
            label={translate.t("search_findings.tab_description.requirements")}
            name="requirements"
            renderAsEditable={props.isEditing}
            type="text"
            validate={[required]}
            visible={validateEmptyField}
          />
        </Col>
      </Row>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <FormGroup>
            <ControlLabel><b>{translate.t("search_findings.tab_description.where")}</b></ControlLabel><br />
            <VulnerabilitiesView
              editMode={props.isEditing && _.includes(["admin", "analyst", "customer"], props.userRole)}
              findingId={props.findingId}
              state="open"
              userRole={props.userRole}
              renderAsEditable={props.isEditing}
              descriptParam={props}
              separatedRow={true}
            />
          </FormGroup>
        </Col>
      </Row>
      <Row>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            className={globalStyle.noResize}
            component={textAreaField}
            currentValue={props.dataset.attackVectorDesc}
            label={translate.t("search_findings.tab_description.attack_vectors")}
            name="attackVectorDesc"
            renderAsEditable={props.isEditing}
            type="text"
            visible={validateEmptyField}
            validate={[required]}
          />
        </Col>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            className={globalStyle.noResize}
            component={textAreaField}
            currentValue={props.dataset.affectedSystems}
            label={translate.t("search_findings.tab_description.affected_systems")}
            name="affectedSystems"
            renderAsEditable={props.isEditing}
            type="text"
            validate={[required]}
            visible={validateEmptyField}
          />
        </Col>
      </Row>
      <Row>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            className={globalStyle.noResize}
            component={textAreaField}
            currentValue={props.dataset.threat}
            label={translate.t("search_findings.tab_description.threat")}
            name="threat"
            renderAsEditable={props.isEditing}
            type="text"
            validate={[required]}
            visible={validateEmptyField}
          />
        </Col>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            className={globalStyle.noResize}
            component={textAreaField}
            currentValue={props.dataset.risk}
            label={translate.t("search_findings.tab_description.risk")}
            name="risk"
            renderAsEditable={props.isEditing}
            type="text"
            visible={props.isEditing && _.includes(["admin", "analyst"], props.userRole)}
          />
        </Col>
      </Row>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <EditableField
            className={globalStyle.noResize}
            component={textAreaField}
            currentValue={props.dataset.recommendation}
            label={translate.t("search_findings.tab_description.recommendation")}
            name="recommendation"
            renderAsEditable={props.isEditing}
            type="text"
            validate={[required]}
            visible={validateEmptyField}
          />
        </Col>
      </Row>
      <Row>
         {/* tslint:disable-next-line jsx-no-multiline-js Necessary for validate conditional */}
        {(!_.isEmpty(props.dataset.compromisedAttributes) && !props.isEditing) || canEditDescription ?
        <Col md={6} sm={12} xs={12}>
          <EditableField
            className={globalStyle.noResize}
            component={textAreaField}
            currentValue={props.dataset.compromisedAttributes}
            label={translate.t("search_findings.tab_description.compromised_attrs")}
            name="compromisedAttributes"
            renderAsEditable={props.isEditing}
            type="text"
          />
        </Col>
        : undefined}
        <Col md={6} sm={12} xs={12}>
          <EditableField
            className={globalStyle.noResize}
            component={textAreaField}
            currentValue={props.dataset.compromisedRecords}
            label={translate.t("search_findings.tab_description.compromised_records")}
            name="compromisedRecords"
            renderAsEditable={props.isEditing}
            type="number"
            validate={[required, numeric]}
            visible={validateEmptyField}
          />
        </Col>
      </Row>
      <Row>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            component={textField}
            currentValue={formatCweUrl(props.dataset.cweUrl)}
            label={translate.t("search_findings.tab_description.weakness")}
            name="cweUrl"
            renderAsEditable={props.isEditing}
            type="number"
            validate={[required, numeric]}
            visible={validateEmptyField}
          />
        </Col>
      </Row>
    </React.Fragment>
  );
};

export const renderFormFields: renderFormFieldsFn = (props: IDescriptionViewProps): JSX.Element => {
  const canEditTreatment: boolean = _.includes(["customer", "customeradmin"], props.userRole);

  return (
    <React.Fragment>
      {renderDescriptionFields(props)}
      {!props.isEditing || (props.isEditing && canEditTreatment) ? TreatmentFieldsView(props) : undefined}
    </React.Fragment>
  );
};
