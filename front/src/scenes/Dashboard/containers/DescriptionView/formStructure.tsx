import _ from "lodash";
import React from "react";
import { Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { default as globalStyle } from "../../../../styles/global.css";
import {
  formatCweUrl,
  formatFindingType,
} from "../../../../utils/formatHelpers";
import { dropdownField, textAreaField, textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { numeric, required, validDraftTitle } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import TreatmentFieldsView from "../../components/treatmentFields";
import { VulnerabilitiesView } from "../../components/Vulnerabilities";
import { IDescriptionViewProps } from "./index";

type renderFormFieldsFn = ((props: IDescriptionViewProps) => JSX.Element);

const renderDescriptionFields: renderFormFieldsFn = (props: IDescriptionViewProps): JSX.Element => {

  const canEditDescription: boolean =
  (props.isEditing && _.includes(["admin", "analyst"], props.userRole));
  const isRequestingVerification: boolean = props.isRequestingVerification || props.isVerifyingRequest;
  const validateEmptyField: boolean = (!props.isEditing || canEditDescription) && !isRequestingVerification;
  const validRole: boolean = _.includes(["admin", "analyst", "customer", "customeradmin"], props.userRole);
  const nTreatmentState: number = props.dataset.historicTreatment.length;
  const { verificationFn } = props;

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
            visible={!props.isEditing && _.includes(["analyst", "admin"], props.userRole) && !isRequestingVerification}
          />
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
            validate={[required, validDraftTitle]}
            visible={props.isEditing && _.includes(["admin", "analyst"], props.userRole)}
          />
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
              editMode={props.isEditing && validRole}
              findingId={props.findingId}
              isRequestVerification={props.isRequestingVerification}
              isVerifyRequest={props.isVerifyingRequest}
              state="open"
              userRole={props.userRole}
              projectName={props.projectName}
              btsUrl={props.dataset.btsUrl}
              lastTreatment={_.last(props.dataset.historicTreatment)}
              separatedRow={true}
              verificationFn={verificationFn}
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
        {(!_.isEmpty(props.dataset.compromisedAttributes) && !props.isEditing && !isRequestingVerification)
          || canEditDescription ?
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
      {/* tslint:disable-next-line jsx-no-multiline-js Necessary for validate conditional */}
      {props.dataset.acceptationApproval === "APPROVED"
      && props.dataset.historicTreatment[nTreatmentState - 1].treatment === "ACCEPTED" ?
      <React.Fragment>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <EditableField
            component={textField}
            currentValue={props.dataset.justification}
            label={translate.t("search_findings.tab_description.acceptation_justification")}
            name="justification"
            renderAsEditable={false}
            type="text"
          />
        </Col>
      </Row>
      <Row>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            component={textField}
            currentValue={props.dataset.acceptationUser}
            label={translate.t("search_findings.tab_description.acceptation_user")}
            name="acceptationUser"
            renderAsEditable={false}
            type="text"
          />
        </Col>
      </Row>
    </React.Fragment> : undefined}
    </React.Fragment>
  );
};

export const renderFormFields: renderFormFieldsFn = (props: IDescriptionViewProps): JSX.Element => {
  const canEditTreatment: boolean = _.includes(["customer", "customeradmin"], props.userRole);
  const shouldRenderEditable: boolean = (!props.isEditing || (props.isEditing && canEditTreatment))
    && !(props.isRequestingVerification || props.isVerifyingRequest);

  return (
    <React.Fragment>
      {renderDescriptionFields(props)}
      {shouldRenderEditable ? <TreatmentFieldsView isTreatmentModal={false} {...props}/> : undefined}
    </React.Fragment>
  );
};
