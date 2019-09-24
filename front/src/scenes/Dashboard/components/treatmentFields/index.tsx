import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import globalStyle from "../../../../styles/global.css";
import {  formatDropdownField } from "../../../../utils/formatHelpers";
import { dateField, dropdownField, textAreaField, textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { isLowerDate, isValidDate, required } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { IDescriptionViewProps } from "../../containers/DescriptionView/index";

type renderFormFieldsFn = ((props: IDescriptionViewProps) => JSX.Element);

const renderTreatmentFields: renderFormFieldsFn = (props: IDescriptionViewProps): JSX.Element => {
    const hasBts: boolean = !_.isEmpty(props.dataset.btsUrl);
    const isNotEditable: boolean = props.isEditing &&
    (props.userRole === "customer" && props.formValues.treatment === "IN PROGRESS");
    const changeRender: boolean = props.isEditing && (props.formValues.treatment === "IN PROGRESS" ||
    props.formValues.treatment === "ACCEPTED");
    const shouldRender: boolean = !props.isEditing && (props.dataset.treatment === "IN PROGRESS" ||
    props.dataset.treatment === "ACCEPTED");

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
        {shouldRender || changeRender ?
          <Col md={6} sm={12} xs={12}>
            <EditableField
              component={dropdownField/* tslint:disable-next-line jsx-no-multiline-js */}
              currentValue={props.formValues.treatment === "ACCEPTED" || isNotEditable ? !props.isEditing ?
                props.dataset.treatmentManager : props.currentUserEmail : props.dataset.treatmentManager}
              label={translate.t("search_findings.tab_description.treatment_mgr")}
              name={"treatmentManager"/* tslint:disable-next-line jsx-no-multiline-js */}
              renderAsEditable={props.userRole === "customeradmin" && props.formValues.treatment !== "ACCEPTED" ?
                props.isEditing : false}
              type="text"
              validate={[...props.formValues.treatment === "IN PROGRESS" ? [required] : []]}
            >
              <option value="" selected={true} />
              {/* tslint:disable-next-line jsx-no-multiline-js Necessary for mapping users into JSX Elements */}
              {props.dataset.userEmails.map(({ email }: { email: string }, index: number): JSX.Element =>
                <option key={index} value={email}>{email}</option>)}
            </EditableField>
          </Col>
        : undefined}
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
      {/* tslint:disable-next-line jsx-no-multiline-js Necessary for validate conditional */}
      {shouldRender || changeRender ?
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
          <Col md={3} sm={12} xs={12}>
            <EditableField
              component={dateField}
              currentValue={props.dataset.acceptanceDate.split(" ")[0]}
              label={translate.t("search_findings.tab_description.acceptance_date")}
              name="acceptanceDate"
              renderAsEditable={props.isEditing}
              type="date"
              validate={[isValidDate, isLowerDate]}
            />
          </Col>
        </Row>
      : undefined}
    </React.Fragment>
    );
  };

export { renderTreatmentFields as TreatmentFieldsView };
