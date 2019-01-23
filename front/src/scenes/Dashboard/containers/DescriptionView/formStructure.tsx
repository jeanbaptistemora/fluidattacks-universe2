import _ from "lodash";
import React from "react";
import globalStyle from "../../../../styles/global.css";
import { dropdownField, textAreaField, textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { FormRows } from "../../components/GenericForm/index";
import { IDescriptionViewProps } from "./index";

export const getFormStructure: ((props: IDescriptionViewProps) => FormRows) =
  (props: IDescriptionViewProps): FormRows => [
    [{
      componentProps: {
        children: (
          <React.Fragment>
            <option value="" selected={true} />
            <option value="Detallado">
              {translate.t("search_findings.tab_description.reportLevel.detailed")}
            </option>
            <option value="General">
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
      visible: true,
    }],
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
      visible: true,
    }],
    [{
      componentProps: {
        children: (
          <React.Fragment>
            <option value="" selected={true} />
            <option value="Anónimo desde Internet">
              {translate.t("search_findings.tab_description.scenario.anon_inter")}
            </option>
            <option value="Anónimo desde Intranet">
              {translate.t("search_findings.tab_description.scenario.anon_intra")}
            </option>
            <option value="Escaneo de Infraestructura">
              {translate.t("search_findings.tab_description.scenario.infra_scan")}
            </option>
            <option value="Usuario de Extranet no autorizado">
              {translate.t("search_findings.tab_description.scenario.unauth_extra")}
            </option>
            <option value="Usuario de Internet autorizado">
              {translate.t("search_findings.tab_description.scenario.auth_inter")}
            </option>
            <option value="Usuario de Internet no autorizado">
              {translate.t("search_findings.tab_description.scenario.unauth_inter")}
            </option>
            <option value="Usuario de Intranet autorizado">
              {translate.t("search_findings.tab_description.scenario.auth_intra")}
            </option>
            <option value="Usuario de Intranet no autorizado">
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
            <option value="Cualquier persona en Internet">
              {translate.t("search_findings.tab_description.actor.any_internet")}
            </option>
            <option value="Cualquier cliente de la organización">
              {translate.t("search_findings.tab_description.actor.any_costumer")}
            </option>
            <option value="Solo algunos clientes de la organización">
              {translate.t("search_findings.tab_description.actor.some_costumer")}
            </option>
            <option value="Cualquier persona con acceso a la estación">
              {translate.t("search_findings.tab_description.actor.any_station")}
            </option>
            <option value="Cualquier empleado de la organización">
              {translate.t("search_findings.tab_description.actor.any_employee")}
            </option>
            <option value="Solo algunos empleados">
              {translate.t("search_findings.tab_description.actor.some_employee")}
            </option>
            <option value="Solo un empleado">
              {translate.t("search_findings.tab_description.actor.one_employee")}
            </option>
          </React.Fragment>),
        component: dropdownField,
        name: "actor",
        validate: [required],
      },
      label: translate.t("search_findings.tab_description.actor.title"),
      renderAsEditable: props.isEditing && _.includes(["admin", "analyst"], props.userRole),
      value: props.dataset.actor,
      visible: true,
    }],
    [{
      componentProps: {
        component: textField,
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
  ];
