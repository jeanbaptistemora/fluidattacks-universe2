import { Button } from "components/Button/index";
import { FluidIcon } from "components/FluidIcon";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import type { Validator } from "redux-form";
import _ from "lodash";
import style from "scenes/Dashboard/components/EvidenceImage/index.css";
import { translate } from "utils/translations/translate";
import {
  ButtonToolbarLeft,
  Col33,
  EvidenceDescription,
  Row,
} from "styles/styledComponents";
import { Field, FormSection } from "redux-form";
import { FileInput, TextArea } from "utils/forms/fields";
import { validEvidenceDescription, validTextField } from "utils/validations";

/* eslint-disable react/require-default-props, react/no-unused-prop-types */
interface IEvidenceImageProps {
  acceptedMimes?: string;
  content: JSX.Element | string;
  date?: string;
  description: string;
  isDescriptionEditable: boolean;
  isEditing: boolean;
  isRemovable?: boolean;
  name: string;
  validate?: Validator | Validator[];
  onClick: () => void;
  onDelete?: () => void;
}
/* eslint-disable react/require-default-props, react/no-unused-prop-types */

const renderForm: (props: IEvidenceImageProps) => JSX.Element = (
  props: IEvidenceImageProps
): JSX.Element => {
  const { onDelete } = props;

  return (
    <FormSection name={props.name}>
      <Field
        accept={props.acceptedMimes}
        component={FileInput}
        id={props.name}
        name={"file"}
        validate={props.validate}
      />
      {props.isDescriptionEditable ? (
        <TooltipWrapper
          id={translate.t("search_findings.tabEvidence.descriptionTooltip.id")}
          message={translate.t(
            "search_findings.tabEvidence.descriptionTooltip"
          )}
          placement={"right"}
        >
          <Field
            component={TextArea}
            name={"description"}
            validate={[validEvidenceDescription, validTextField]}
          />
        </TooltipWrapper>
      ) : (
        <p>{props.description}</p>
      )}
      {props.isRemovable === true ? (
        <ButtonToolbarLeft>
          <TooltipWrapper
            id={translate.t("search_findings.tabEvidence.removeTooltip.id")}
            message={translate.t("search_findings.tabEvidence.removeTooltip")}
          >
            <Button onClick={onDelete}>
              <FluidIcon icon={"delete"} />
              &nbsp;{translate.t("search_findings.tabEvidence.remove")}
            </Button>
          </TooltipWrapper>
        </ButtonToolbarLeft>
      ) : undefined}
    </FormSection>
  );
};

const EvidenceImage: React.FC<IEvidenceImageProps> = (
  props: IEvidenceImageProps
): JSX.Element => {
  const { content, isEditing, description, date, onClick } = props;
  const handleClick: () => void = React.useCallback((): void => {
    onClick();
  }, [onClick]);

  return (
    <React.StrictMode>
      <Col33>
        <div>
          <div className={style.imgContainer}>
            {typeof content === "string" ? (
              /* eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-noninteractive-element-interactions */
              <img
                alt={""}
                className={style.img}
                onClick={handleClick}
                src={content}
              />
            ) : (
              React.cloneElement(content, {
                className: style.img,
                onClick: handleClick,
              })
            )}
          </div>
          <div className={style.description}>
            <Row>
              <label>
                <b>{translate.t("search_findings.tabEvidence.detail")}</b>
              </label>
            </Row>
            <Row>
              {isEditing ? (
                renderForm(props)
              ) : (
                <React.Fragment>
                  <EvidenceDescription>{description}</EvidenceDescription>
                  {_.isEmpty(date) ? undefined : (
                    <EvidenceDescription>
                      {translate.t("search_findings.tabEvidence.date")}&nbsp;
                      {date?.split(" ")[0]}
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

export { EvidenceImage };
