import _ from "lodash";
import React from "react";
import globalStyle from "../../../../styles/global.css";
import { formatCweUrl, formatDropdownField } from "../../../../utils/formatHelpers";
import { dropdownField, textAreaField, textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { numeric, required } from "../../../../utils/validations";
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


const renderDetailedFields: ((props: IDescriptionViewProps) => FormRows) =
  (props: IDescriptionViewProps): FormRows => [
    [renderCustomerCodeField(props), renderCustomerProjectField(props)],
  ];

export const getFormStructure: ((props: IDescriptionViewProps) => FormRows) =
  (props: IDescriptionViewProps): FormRows => [
    [renderReportLevelField(props)],
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
            <option value="Anónimo desde internet">
              {translate.t("search_findings.tab_description.scenario.anon_inter")}
            </option>
            <option value="Anónimo desde intranet">
              {translate.t("search_findings.tab_description.scenario.anon_intra")}
            </option>
            <option value="Extranet usuario autorizado">
              {translate.t("search_findings.tab_description.scenario.auth_extra")}
            </option>
            <option value="Extranet usuario no autorizado">
              {translate.t("search_findings.tab_description.scenario.unauth_extra")}
            </option>
            <option value="Internet usuario autorizado">
              {translate.t("search_findings.tab_description.scenario.auth_inter")}
            </option>
            <option value="Internet usuario no autorizado">
              {translate.t("search_findings.tab_description.scenario.unauth_inter")}
            </option>
            <option value="Intranet usuario autorizado">
              {translate.t("search_findings.tab_description.scenario.auth_intra")}
            </option>
            <option value="Intranet usuario no autorizado">
              {translate.t("search_findings.tab_description.scenario.unauth_intra")}
            </option>
          </React.Fragment>),
        component: dropdownField,
        name: "scenario",
        validate: [required],
      },
      label: translate.t("search_findings.tab_description.scenario.title"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: props.dataset.scenario,
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
        name: "threat",
        type: "text",
        validate: [required],
      },
      label: translate.t("search_findings.tab_description.threat"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: props.dataset.threat,
      visible: true,
    }],
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
