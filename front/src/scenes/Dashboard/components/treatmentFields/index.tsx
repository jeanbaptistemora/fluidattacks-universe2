import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import globalStyle from "../../../../styles/global.css";
import {  formatDropdownField } from "../../../../utils/formatHelpers";
import { dropdownField, textAreaField, textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { IDescriptionViewProps } from "../../containers/DescriptionView/index";

type renderFormFieldsFn = ((props: IDescriptionViewProps) => JSX.Element);

const renderTreatmentFields: renderFormFieldsFn = (props: IDescriptionViewProps): JSX.Element => {
    const hasBts: boolean = !_.isEmpty(props.dataset.btsUrl);

    return(
    <React.Fragment>
      <Row>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            component={dropdownField}
            currentValue={translate.t(formatDropdownField(props.dataset.treatment))}
            label={translate.t("search_findings.tab_description.treatment.title")}
            name="treatment"
            renderAsEditable={props.isEditing}
            type="text"
            validate={[required]}
          >
            <option value="" selected={true} />
            <option value="ACCEPTED">{translate.t("search_findings.tab_description.treatment.accepted")}</option>
            <option value="NEW">{translate.t("search_findings.tab_description.treatment.new")}</option>
            <option value="IN PROGRESS">{translate.t("search_findings.tab_description.treatment.in_progress")}</option>
          </EditableField>
        </Col>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            component={dropdownField}
            currentValue={props.dataset.treatmentManager}
            label={translate.t("search_findings.tab_description.treatment_mgr")}
            name="treatmentManager"
            renderAsEditable={props.isEditing}
            type="text"
            validate={[...props.formValues.treatment === "IN PROGRESS" ? [required] : []]}
            visible={!props.isEditing || (props.isEditing && props.formValues.treatment === "IN PROGRESS")}
          >
            <option value="" selected={true} />
            {/* tslint:disable-next-line jsx-no-multiline-js Necessary for mapping users into JSX Elements */}
            {props.dataset.userEmails.map(({ email }: { email: string }, index: number): JSX.Element =>
              <option key={index} value={email}>{email}</option>)}
          </EditableField>
        </Col>
        <Col md={12} sm={12} xs={12}>
          <EditableField
            component={textField}
            currentValue={props.dataset.btsUrl}
            label={translate.t("search_findings.tab_description.bts")}
            name="btsUrl"
            renderAsEditable={props.isEditing}
            type="text"
            visible={!props.isEditing && hasBts || (props.isEditing && props.formValues.treatment === "IN PROGRESS")}
          />
        </Col>
      </Row>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <EditableField
            className={globalStyle.noResize}
            component={textAreaField}
            currentValue={props.dataset.treatmentJustification}
            label={translate.t("search_findings.tab_description.treatment_just")}
            name="treatmentJustification"
            renderAsEditable={props.isEditing}
            type="text"
            validate={[required]}
          />
        </Col>
      </Row>
    </React.Fragment>
    );
  };

export { renderTreatmentFields as TreatmentFieldsView };
