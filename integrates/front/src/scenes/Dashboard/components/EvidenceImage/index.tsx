/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that renders the form
 */
import _ from "lodash";
import React from "react";
import { Field, FormSection, Validator } from "redux-form";

import { Button } from "components/Button/index";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { default as style } from "scenes/Dashboard/components/EvidenceImage/index.css";
import { ButtonToolbarLeft, Col33, EvidenceDescription, Row } from "styles/styledComponents";
import { FileInput, TextArea } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { validEvidenceDescription, validTextField } from "utils/validations";

interface IEvidenceImageProps {
  acceptedMimes?: string;
  content: string | JSX.Element;
  date?: string;
  description: string;
  isDescriptionEditable: boolean;
  isEditing: boolean;
  isRemovable?: boolean;
  name: string;
  validate?: Validator | Validator[];
  onClick(): void;
  onDelete?(): void;
}

const renderForm: ((props: IEvidenceImageProps) => JSX.Element) = (props: IEvidenceImageProps): JSX.Element => {
  const { onDelete } = props;

  return (
    <FormSection name={props.name}>
      <Field
        name="file"
        id={props.name}
        component={FileInput}
        accept={props.acceptedMimes}
        validate={props.validate}
      />
      {props.isDescriptionEditable
        ?
          <TooltipWrapper
            id={translate.t("search_findings.tab_evidence.description_tooltip.id")}
            message={translate.t("search_findings.tab_evidence.description_tooltip")}
            placement="right"
          >
            <Field
              name="description"
              component={TextArea}
              validate={[validEvidenceDescription, validTextField]}
            />
          </TooltipWrapper>
        : <p>{props.description}</p>}
      {props.isRemovable === true
        ? <ButtonToolbarLeft>
          <TooltipWrapper
            id={translate.t("search_findings.tab_evidence.remove_tooltip.id")}
            message={translate.t("search_findings.tab_evidence.remove_tooltip")}
          >
            <Button onClick={onDelete}>
              <FluidIcon icon="delete" />
              &nbsp;{translate.t("search_findings.tab_evidence.remove")}
            </Button>
          </TooltipWrapper>
        </ButtonToolbarLeft>
        : undefined}
    </FormSection>
  );
};

export const evidenceImage: React.FC<IEvidenceImageProps> = (props: IEvidenceImageProps): JSX.Element => {
  const handleClick: (() => void) = (): void => { props.onClick(); };

  return (
    <React.StrictMode>
      <Col33>
        <div>
          <div className={style.imgContainer}>
            {typeof (props.content) === "string"
              ? <img src={props.content} className={style.img} onClick={handleClick} />
              : React.cloneElement(props.content, { className: style.img, onClick: handleClick })}
          </div>
          <div className={style.description}>
            <Row>
              <label><b>{translate.t("search_findings.tab_evidence.detail")}</b></label>
            </Row>
            <Row>
              {props.isEditing ? renderForm(props) : (
                <React.Fragment>
                  <EvidenceDescription>
                    {props.description}
                  </EvidenceDescription>
                  {_.isEmpty(props.date) ? undefined : (
                    <EvidenceDescription>
                      {translate.t("search_findings.tab_evidence.date")}&nbsp;
                      {props.date?.split(" ")[0]}
                    </EvidenceDescription>
                  )}
                </React.Fragment>
              )}
            </Row>
          </div>
        </div>
      </Col33>
    </React.StrictMode>
  );
};
