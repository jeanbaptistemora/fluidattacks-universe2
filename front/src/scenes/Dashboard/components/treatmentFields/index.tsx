import _ from "lodash";
import React from "react";
import { Checkbox, Col, Row } from "react-bootstrap";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { ConfirmDialog } from "../../../../components/ConfirmDialog";
import store from "../../../../store/index";
import { default as globalStyle } from "../../../../styles/global.css";
import { formatDropdownField } from "../../../../utils/formatHelpers";
import { dateField, dropdownField, textAreaField, textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { isLowerOrEqualDate, isValidDate, isValidVulnSeverity, numeric, required } from "../../../../utils/validations";
import { openConfirmDialog } from "../../actions";
import { EditableField } from "../../components/EditableField";
import { IDescriptionViewProps } from "../../containers/DescriptionView/index";

type renderFormFieldsFn = ((props: IDescriptionViewProps) => JSX.Element);
const openDialog: (() => void) = (): void => {
  store.dispatch(openConfirmDialog("advertisement"));
};

const treatmentFieldsView: renderFormFieldsFn = (props: IDescriptionViewProps): JSX.Element => {
    let formTreatmentValue: string = !_.isUndefined(props.formValues.treatmentVuln) ?
    props.formValues.treatmentVuln : props.formValues.treatment;
    if (formTreatmentValue === "ACCEPTED_UNDEFINED") {
      formTreatmentValue = "ACCEPTED";
    }
    const hasBts: boolean = !_.isEmpty(props.dataset.btsUrl);
    const isNotEditable: boolean = props.isEditing && props.userRole === "customer";
    const treatmentAccepted: boolean = formTreatmentValue === "ACCEPTED";
    const changeRender: boolean = props.isEditing && (formTreatmentValue === "IN PROGRESS" ||
    treatmentAccepted);
    const shouldRender: boolean = !props.isEditing && (formTreatmentValue === "IN PROGRESS" ||
    props.dataset.treatment === "ACCEPTED");
    const isEditable: boolean = props.isEditing && !props.isTreatmentModal;
    const shouldRenderField: boolean = shouldRender || changeRender;

    /* tslint:disable-next-line cyclomatic-complexity Necessary because this function has a complexity of 21 > 20 */
    const renderVulnFields: (() => JSX.Element) = (): JSX.Element => (
      <React.Fragment>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            component={textField}
            currentValue={!_.isUndefined(props.dataset.tag) ? props.dataset.tag : ""}
            label={translate.t("search_findings.tab_description.tag")}
            name="tag"
            renderAsEditable={props.isEditing}
            type="text"
          />
        </Col>
        <Col md={6} sm={12} xs={12}>
          <EditableField
            component={textField}
            currentValue={!_.isUndefined(props.dataset.severity) ? props.dataset.severity : ""}
            label={translate.t("search_findings.tab_description.severity")}
            name="severity"
            renderAsEditable={props.isEditing}
            type="number"
            validate={[isValidVulnSeverity, numeric]}
          />
        </Col>
      </React.Fragment>
    );

    return(
    <React.Fragment>
      <Row>
        <Col md={6} sm={8} xs={12}>
          <EditableField
            component={dropdownField}
            currentValue={translate.t(formatDropdownField(formTreatmentValue))}
            label={translate.t("search_findings.tab_description.treatment.title")}
            name="treatment"
            renderAsEditable={isEditable}
            type="text"
            validate={[required]}
          >
            <option value="NEW">{translate.t("search_findings.tab_description.treatment.new")}</option>
            <option value="IN PROGRESS">{translate.t("search_findings.tab_description.treatment.in_progress")}</option>
            <option value="ACCEPTED">{translate.t("search_findings.tab_description.treatment.accepted")}</option>
            <option hidden={true} value="ACCEPTED_UNDEFINED">
              {translate.t("search_findings.tab_description.treatment.accepted_undefined")}
            </option>

          </EditableField>
        </Col>
        {/* tslint:disable-next-line jsx-no-multiline-js Necessary for conditionals into JSX Elements */}
        {treatmentAccepted ?
          <Col md={6} sm={4} xs={4} hidden={true}>
            <Checkbox
              checked={false}
              onClick={openDialog}
            >
              {translate.t("search_findings.tab_description.checkbox_accepted")}
            </Checkbox>
          </Col>
          : undefined}
        <ConfirmDialog
          closeOnProceed={true}
          name="advertisement"
          message={translate.t("search_findings.tab_description.approval_message")}
          onlyProceed={true}
          title={translate.t("search_findings.tab_description.approval_title")}
        />
        {shouldRenderField && props.isTreatmentModal ?
          <Col md={6} sm={12} xs={12}>
            <EditableField
              component={dropdownField/* tslint:disable-next-line jsx-no-multiline-js */}
              currentValue={treatmentAccepted || isNotEditable ? !props.isEditing ?
                props.dataset.treatmentManager : props.currentUserEmail : props.dataset.treatmentManager}
              label={translate.t("search_findings.tab_description.treatment_mgr")}
              name={"treatmentManager"/* tslint:disable-next-line jsx-no-multiline-js */}
              renderAsEditable={props.userRole === "customeradmin" && !treatmentAccepted ?
                props.isEditing : false}
              type="text"
              validate={[...formTreatmentValue === "IN PROGRESS" ? [required] : []]}
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
            renderAsEditable={isEditable}
            type="text"
            visible={hasBts || (props.isEditing && !props.isTreatmentModal)}
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
              renderAsEditable={isEditable}
              type="text"
              validate={[required]}
              visible={shouldRenderField}
            />
          </Col>
        </Row>
        <Row>
          <Col md={4} sm={12} xs={12}>
            <EditableField
              component={dateField}
              currentValue={props.dataset.acceptanceDate.split(" ")[0]}
              label={translate.t("search_findings.tab_description.acceptance_date")}
              name="acceptanceDate"
              renderAsEditable={isEditable}
              type="date"
              validate={[isValidDate, isLowerOrEqualDate]}
              visible={(treatmentAccepted)}
            />
          </Col>
        </Row>
        <Row>
          {props.isTreatmentModal ? renderVulnFields() : undefined}
        </Row>
    </React.Fragment>
    );
  };

const enhance: InferableComponentEnhancer<{}> = lifecycle<IDescriptionViewProps, {}>({
    shouldComponentUpdate(nextProps: IDescriptionViewProps, nextState: {}): boolean {
      if (nextProps.isEditing && !_.isUndefined(nextProps.formValues.treatmentVuln) && !nextProps.isTreatmentModal) {

        return false;
      }

      return true;
    },
  });

export = enhance(treatmentFieldsView);
