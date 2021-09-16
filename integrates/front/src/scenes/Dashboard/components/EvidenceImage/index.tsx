import { Field } from "formik";
import type { FieldValidator } from "formik";
import _ from "lodash";
import React, { cloneElement, useCallback } from "react";

import { Button } from "components/Button/index";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import style from "scenes/Dashboard/components/EvidenceImage/index.css";
import {
  ButtonToolbarLeft,
  Col33,
  EvidenceDescription,
  Row,
} from "styles/styledComponents";
import { FormikFileInput, FormikTextArea } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  validEvidenceDescription,
  validTextField,
} from "utils/validations";

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
  validate?: FieldValidator | FieldValidator[] | unknown;
  onClick: () => void;
  onDelete?: () => void;
}
/* eslint-disable react/require-default-props, react/no-unused-prop-types */

const renderForm: (props: IEvidenceImageProps) => JSX.Element = (
  props: IEvidenceImageProps
): JSX.Element => {
  const { onDelete } = props;

  const getFieldName = (fieldName: string): string => {
    const { name } = props;

    return name ? `${name}.${fieldName}` : fieldName;
  };

  return (
    <div>
      <Field
        accept={props.acceptedMimes}
        component={FormikFileInput}
        id={props.name}
        name={getFieldName("file")}
        validate={props.validate}
      />
      {props.isDescriptionEditable ? (
        <TooltipWrapper
          id={translate.t("searchFindings.tabEvidence.descriptionTooltip.id")}
          message={translate.t("searchFindings.tabEvidence.descriptionTooltip")}
          placement={"right"}
        >
          <Field
            component={FormikTextArea}
            name={getFieldName("description")}
            validate={composeValidators([
              validEvidenceDescription,
              validTextField,
            ])}
          />
        </TooltipWrapper>
      ) : (
        <p>{props.description}</p>
      )}
      {props.isRemovable === true ? (
        <ButtonToolbarLeft>
          <TooltipWrapper
            id={translate.t("searchFindings.tabEvidence.removeTooltip.id")}
            message={translate.t("searchFindings.tabEvidence.removeTooltip")}
          >
            <Button onClick={onDelete}>
              <FluidIcon icon={"delete"} />
              &nbsp;{translate.t("searchFindings.tabEvidence.remove")}
            </Button>
          </TooltipWrapper>
        </ButtonToolbarLeft>
      ) : undefined}
    </div>
  );
};

const EvidenceImage: React.FC<IEvidenceImageProps> = (
  props: IEvidenceImageProps
): JSX.Element => {
  const { content, isEditing, description, date, onClick } = props;
  const handleClick: () => void = useCallback((): void => {
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
              cloneElement(content, {
                className: style.img,
                onClick: handleClick,
              })
            )}
          </div>
          <div className={style.description}>
            <Row>
              <label>
                <b>{translate.t("searchFindings.tabEvidence.detail")}</b>
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
                      {translate.t("searchFindings.tabEvidence.date")}&nbsp;
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
