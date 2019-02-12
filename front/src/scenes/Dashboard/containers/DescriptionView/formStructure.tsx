import _ from "lodash";
import React from "react";
import globalStyle from "../../../../styles/global.css";
import { formatCweUrl, formatDropdownField } from "../../../../utils/formatHelpers";
import { dropdownField, textAreaField, textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { numberBetween, numeric, required } from "../../../../utils/validations";
import { FormRows, IEditableField } from "../../components/GenericForm/index";
import { vulnsView as VulnerabilitiesView } from "../../components/Vulnerabilities";
import { IDescriptionViewProps } from "./index";

const renderReportLevelField: ((props: IDescriptionViewProps) => IEditableField) =
  (props: IDescriptionViewProps): IEditableField => ({
    componentProps: {
      children: (
        <React.Fragment>
          <option value="" selected={true} />
          <option value="DETAILED">
            {translate.t("search_findings.tab_description.reportLevel.detailed")}
          </option>
          <option value="GENERAL">
            {translate.t("search_findings.tab_description.reportLevel.general")}
          </option>
        </React.Fragment>),
      component: dropdownField,
      name: "reportLevel",
      validate: [required],
    },
    label: translate.t("search_findings.tab_description.reportLevel.title"),
    renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
    value: props.dataset.reportLevel,
    visible: props.isEditing,
  });

const renderFindingTypeField: ((props: IDescriptionViewProps) => IEditableField) =
  (props: IDescriptionViewProps): IEditableField => ({
    componentProps: {
      children: (
        <React.Fragment>
          <option value="" selected={true} />
          <option value="SECURITY">{translate.t("search_findings.tab_description.type.security")}</option>
          <option value="HYGIENE">{translate.t("search_findings.tab_description.type.hygiene")}</option>
        </React.Fragment>),
      component: dropdownField,
      name: "type",
      validate: [required],
    },
    label: translate.t("search_findings.tab_description.type.title"),
    renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
    value: translate.t(`search_findings.tab_description.type.${props.dataset.type.toLowerCase()}`),
    visible: true,
  });

const renderTreatmentMgrField: ((props: IDescriptionViewProps) => IEditableField) =
  (props: IDescriptionViewProps): IEditableField => {
    const options: JSX.Element[] =
      props.dataset.userEmails.map(({ email }: { email: string }, index: number): JSX.Element =>
        <option key={index} value={email}>{email}</option>,
      );

    return {
      componentProps: {
        children: (
          <React.Fragment>
            <option value="" selected={true} />
            {options}
          </React.Fragment>),
        component: dropdownField,
        name: "treatmentManager",
        validate: [...props.formValues.treatment === "Remediar" ? [required] : []],
      },
      label: translate.t("search_findings.tab_description.treatment_mgr"),
      renderAsEditable: props.isEditing && _.includes(["customer", "customeradmin"], props.userRole),
      value: props.dataset.treatmentManager,
      visible: !props.isEditing || (props.isEditing && props.formValues.treatment === "Remediar"),
    };
  };

const renderCustomerCodeField: ((props: IDescriptionViewProps) => IEditableField) =
  (props: IDescriptionViewProps): IEditableField => ({
    componentProps: {
      component: textField,
      name: "clientCode",
      type: "text",
      validate: [required],
    },
    label: translate.t("search_findings.tab_description.customer_project_code"),
    renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
    value: props.dataset.clientCode,
    visible: props.isEditing,
  });

const renderCustomerProjectField: ((props: IDescriptionViewProps) => IEditableField) =
  (props: IDescriptionViewProps): IEditableField => ({
    componentProps: {
      component: textField,
      name: "clientProject",
      type: "text",
      validate: [required],
    },
    label: translate.t("search_findings.tab_description.customer_project_name"),
    renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
    value: props.dataset.clientCode,
    visible: props.isEditing,
  });

const renderProbabilityField: ((props: IDescriptionViewProps) => IEditableField) =
  (props: IDescriptionViewProps): IEditableField => ({
    componentProps: {
      children: (
        <React.Fragment>
          <option value="" selected={true} />
          <option value="100% Vulnerado Anteriormente">
            {translate.t("search_findings.tab_description.probability.100")}
          </option>
          <option value="75% Fácil de vulnerar">
            {translate.t("search_findings.tab_description.probability.75")}
          </option>
          <option value="50% Posible de vulnerar">
            {translate.t("search_findings.tab_description.probability.50")}
          </option>
          <option value="25% Difícil de vulnerar">
            {translate.t("search_findings.tab_description.probability.25")}
          </option>
        </React.Fragment>),
      component: dropdownField,
      name: "probability",
      validate: [required],
    },
    label: translate.t("search_findings.tab_description.probability.title"),
    renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
    value: props.dataset.probability,
    visible: props.isEditing,
  });

const severityBetween: ((value: number) => string | undefined) = numberBetween(0, 5);
const renderSeverityField: ((props: IDescriptionViewProps) => IEditableField) =
  (props: IDescriptionViewProps): IEditableField => ({
    componentProps: {
      component: textField,
      name: "detailedSeverity",
      type: "number",
      validate: [required, severityBetween],
    },
    label: translate.t("search_findings.tab_description.severity"),
    renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
    value: props.dataset.probability,
    visible: props.isEditing,
  });

const calcRiskLevel: ((probability: string, severity: number) => string) =
  (probability: string, severity: number): string => {
    const probabilityValue: number = Number(probability
      .substring(0, 3)
      .replace("%", ""));

    return ((probabilityValue / 100) * severity).toFixed(1);
  };

const renderRiskLevel: ((props: IDescriptionViewProps) => IEditableField) =
  (props: IDescriptionViewProps): IEditableField => ({
    componentProps: {
      component: textField,
      disabled: true,
      name: "riskLevel",
      type: "number",
    },
    label: translate.t("search_findings.tab_description.risk_level"),
    renderAsEditable: false,
    value: calcRiskLevel(props.formValues.probability, props.formValues.detailedSeverity),
    visible: props.isEditing,
  });

const renderAmbitField: ((props: IDescriptionViewProps) => IEditableField) =
  (props: IDescriptionViewProps): IEditableField => ({
    componentProps: {
      children: (
        <React.Fragment>
          <option value="" selected={true} />
          <option value="Aplicaciones">
            {translate.t("search_findings.tab_description.ambit.applications")}
          </option>
          <option value="Bases de Datos">
            {translate.t("search_findings.tab_description.ambit.databases")}
          </option>
          <option value="Código fuente">
            {translate.t("search_findings.tab_description.ambit.sourcecode")}
          </option>
          <option value="Infraestructura">
            {translate.t("search_findings.tab_description.ambit.infra")}
          </option>
        </React.Fragment>),
      component: dropdownField,
      name: "ambit",
      validate: [required],
    },
    label: translate.t("search_findings.tab_description.ambit.title"),
    renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
    value: props.dataset.probability,
    visible: props.isEditing,
  });

const renderCategoryField: ((props: IDescriptionViewProps) => IEditableField) =
  (props: IDescriptionViewProps): IEditableField => ({
    componentProps: {
      children: (
        <React.Fragment>
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
        </React.Fragment>),
      component: dropdownField,
      name: "category",
      validate: [required],
    },
    label: translate.t("search_findings.tab_description.category.title"),
    renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
    value: props.dataset.probability,
    visible: props.isEditing,
  });

const renderRiskField: ((props: IDescriptionViewProps) => IEditableField) =
  (props: IDescriptionViewProps): IEditableField => ({
    componentProps: {
      className: globalStyle.noResize,
      component: textAreaField,
      name: "risk",
      type: "text",
      validate: [required],
    },
    label: translate.t("search_findings.tab_description.risk"),
    renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
    value: props.dataset.risk,
    visible: props.isEditing && props.formValues.reportLevel === "DETAILED",
  });

const renderDetailedFields: ((props: IDescriptionViewProps) => FormRows) =
  (props: IDescriptionViewProps): FormRows => [
    [renderCustomerCodeField(props), renderCustomerProjectField(props)],
    [renderProbabilityField(props), renderSeverityField(props), renderRiskLevel(props)],
    [renderAmbitField(props), renderCategoryField(props)],
  ];

const renderAnalystEditableFields: ((props: IDescriptionViewProps) => FormRows) =
  (props: IDescriptionViewProps): FormRows => [
    [renderReportLevelField(props), renderFindingTypeField(props)],
    [{
      componentProps: {
        component: textField,
        name: "title",
        type: "text",
        validate: [required],
      },
      label: translate.t("search_findings.tab_description.title"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: props.dataset.title,
      visible: props.isEditing,
    }],
    ...(props.formValues.reportLevel === "DETAILED" ? renderDetailedFields(props) : []),
    [{
      componentProps: {
        children: (
          <React.Fragment>
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
          </React.Fragment>),
        component: dropdownField,
        name: "scenario",
        validate: [required],
      },
      label: translate.t("search_findings.tab_description.scenario.title"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: translate.t(formatDropdownField(props.dataset.scenario)),
      visible: true,
    },
     {
      componentProps: {
        children: (
          <React.Fragment>
            <option value="" selected={true} />
            <option value="ANYONE_INTERNET">
              {translate.t("search_findings.tab_description.actor.any_internet")}
            </option>
            <option value="ANY_COSTUMER">
              {translate.t("search_findings.tab_description.actor.any_costumer")}
            </option>
            <option value="SOME_CUSTOMERS">
              {translate.t("search_findings.tab_description.actor.some_costumer")}
            </option>
            <option value="ANYONE_WORKSTATION">
              {translate.t("search_findings.tab_description.actor.any_station")}
            </option>
            <option value="ANY_EMPLOYEE">
              {translate.t("search_findings.tab_description.actor.any_employee")}
            </option>
            <option value="SOME_EMPLOYEES">
              {translate.t("search_findings.tab_description.actor.some_employee")}
            </option>
            <option value="ONE_EMPLOYEE">
              {translate.t("search_findings.tab_description.actor.one_employee")}
            </option>
          </React.Fragment>),
        component: dropdownField,
        name: "actor",
        validate: [required],
      },
      label: translate.t("search_findings.tab_description.actor.title"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: translate.t(formatDropdownField(props.dataset.actor)),
      visible: true,
    }],
    [{
      componentProps: {
        className: globalStyle.noResize,
        component: textAreaField,
        name: "description",
        type: "text",
        validate: [required],
      },
      label: translate.t("search_findings.tab_description.description"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: props.dataset.description,
      visible: true,
    }],
    [{
      componentProps: {
        className: globalStyle.noResize,
        component: textAreaField,
        name: "requirements",
        type: "text",
        validate: [required],
      },
      label: translate.t("search_findings.tab_description.requirements"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: props.dataset.requirements,
      visible: true,
    }],
    [{
      customElement: (
        <VulnerabilitiesView
          dataInputs={[]}
          dataLines={[]}
          dataPorts={[]}
          releaseDate={props.dataset.releaseDate}
          editMode={props.isEditing && _.includes(["admin", "analyst"], props.userRole)}
          findingId={props.findingId}
          state="open"
          userRole={props.userRole}
        />),
      label: translate.t("search_findings.tab_description.where"),
      visible: true,
    }],
    [{
      componentProps: {
        className: globalStyle.noResize,
        component: textAreaField,
        name: "attackVector",
        type: "text",
        validate: [required],
      },
      label: translate.t("search_findings.tab_description.attack_vectors"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: props.dataset.attackVector,
      visible: true,
    },
     {
       componentProps: {
         className: globalStyle.noResize,
         component: textAreaField,
         name: "affectedSystems",
         type: "text",
         validate: [required],
       },
       label: translate.t("search_findings.tab_description.affected_systems"),
       renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
       value: props.dataset.affectedSystems,
       visible: true,
     }],
    [{
      componentProps: {
        className: globalStyle.noResize,
        component: textAreaField,
        name: "threat",
        type: "text",
        validate: [required],
      },
      label: translate.t("search_findings.tab_description.threat"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: props.dataset.threat,
      visible: true,
    },
     renderRiskField(props)],
    [{
      componentProps: {
        className: globalStyle.noResize,
        component: textAreaField,
        name: "recommendation",
        type: "text",
        validate: [required],
      },
      label: translate.t("search_findings.tab_description.recommendation"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: props.dataset.recommendation,
      visible: true,
    }],
    [{
      componentProps: {
        className: globalStyle.noResize,
        component: textAreaField,
        name: "compromisedAttributes",
        type: "text",
      },
      label: translate.t("search_findings.tab_description.compromised_attrs"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: props.dataset.compromisedAttributes,
      visible: true,
    },
     {
      componentProps: {
        className: globalStyle.noResize,
        component: textAreaField,
        name: "compromisedRecords",
        type: "text",
        validate: [required, numeric],
      },
      label: translate.t("search_findings.tab_description.compromised_records"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: props.dataset.compromisedRecords,
      visible: true,
    }],
    [{
      componentProps: {
        component: textField,
        name: "cweUrl",
        type: "number",
        validate: [required, numeric],
      },
      label: translate.t("search_findings.tab_description.weakness"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: formatCweUrl(props.dataset.cweUrl),
      visible: true,
    },
     {
      componentProps: {
        component: textField,
        name: "kbUrl",
        type: "text",
      },
      label: translate.t("search_findings.tab_description.kb"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: props.dataset.kbUrl,
      visible: props.dataset.kbUrl !== "" || props.isEditing,
    }],
  ];

const renderCustomerEditableFields: ((props: IDescriptionViewProps) => FormRows) =
  (props: IDescriptionViewProps): FormRows => [
    [{
      componentProps: {
        component: textField,
        name: "btsUrl",
        type: "text",
      },
      label: translate.t("search_findings.tab_description.bts"),
      renderAsEditable: props.isEditing && _.includes(["customer", "customeradmin"], props.userRole),
      value: props.dataset.btsUrl,
      visible: true,
    }],
    [{
      componentProps: {
        children: (
          <React.Fragment>
            <option value="" selected={true} />
            <option value="Asumido">
              {translate.t("search_findings.tab_description.treatment.assumed")}
            </option>
            <option value="Nuevo">
              {translate.t("search_findings.tab_description.treatment.new")}
            </option>
            <option value="Remediar">
              {translate.t("search_findings.tab_description.treatment.in_progress")}
            </option>
          </React.Fragment>),
        component: dropdownField,
        name: "treatment",
        validate: [required],
      },
      label: translate.t("search_findings.tab_description.treatment.title"),
      renderAsEditable: props.isEditing && _.includes(["customer", "customeradmin"], props.userRole),
      value: props.dataset.treatment,
      visible: true,
    },
     renderTreatmentMgrField(props)],
    [{
      componentProps: {
        className: globalStyle.noResize,
        component: textAreaField,
        name: "treatmentJustification",
        type: "text",
        validate: [required],
      },
      label: translate.t("search_findings.tab_description.treatment_just"),
      renderAsEditable: props.isEditing && _.includes(["customer", "customeradmin"], props.userRole),
      value: props.dataset.treatmentJustification,
      visible: true,
    }],
  ];

export const getFormStructure: ((props: IDescriptionViewProps) => FormRows) =
  (props: IDescriptionViewProps): FormRows => [
    ...(!props.isEditing || (props.isEditing && _.includes(["admin", "analyst"], props.userRole))
      ? renderAnalystEditableFields(props) : []),
    ...(!props.isEditing || (props.isEditing && _.includes(["customer", "customeradmin"], props.userRole))
      ? renderCustomerEditableFields(props) : []),
  ];
