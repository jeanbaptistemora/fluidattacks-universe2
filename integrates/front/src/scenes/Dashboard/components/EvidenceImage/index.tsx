/* eslint-disable react/jsx-props-no-spreading, react/no-multi-comp */
import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FieldValidator } from "formik";
import { Field, useField, useFormikContext } from "formik";
import _ from "lodash";
import React, { cloneElement, useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button/index";
import { Tooltip } from "components/Tooltip";
import style from "scenes/Dashboard/components/EvidenceImage/index.css";
import type { IEvidenceItem } from "scenes/Dashboard/containers/EvidenceView/types";
import { Col33, EvidenceDescription, Row } from "styles/styledComponents";
import { FormikFileInput, FormikTextArea } from "utils/forms/fields";
import {
  composeValidators,
  isValidEvidenceDescription,
  maxLength,
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
  /*
   * Can also be of types FieldValidator | FieldValidator[] from the Formik
   * library but the unknown type overrides it
   */
  validate?: unknown;
  onClick: () => void;
  onDelete?: () => void;
  shouldPreviewValidation: FieldValidator[];
  shouldPreview: boolean;
}
/* eslint-disable react/require-default-props, react/no-unused-prop-types */

const MAX_DESCRIPTION_LENGTH: number = 5000;
const maxDescriptionLength: ConfigurableValidator = maxLength(
  MAX_DESCRIPTION_LENGTH
);

const RenderForm: React.FC<IEvidenceImageProps> = ({
  acceptedMimes,
  shouldPreview,
  shouldPreviewValidation,
  description,
  isDescriptionEditable,
  isRemovable = false,
  name,
  onDelete,
  validate,
}: IEvidenceImageProps): JSX.Element => {
  const { t } = useTranslation();
  const getFieldName = (fieldName: string): string => {
    return name ? `${name}.${fieldName}` : fieldName;
  };
  const { initialValues } = useFormikContext<Record<string, IEvidenceItem>>();
  const [fileValue, ,] = useField(getFieldName("file"));
  const validEvidenceDescription: FieldValidator = isValidEvidenceDescription(
    initialValues[name].url,
    fileValue.value
  );

  return (
    <div>
      <Field
        accept={acceptedMimes}
        component={FormikFileInput}
        id={name}
        multiple={false}
        name={getFieldName("file")}
        shouldPreview={shouldPreview && isRemovable}
        shouldPreviewValidation={shouldPreviewValidation}
        validate={validate}
      />
      {isDescriptionEditable ? (
        <Tooltip
          id={t("searchFindings.tabEvidence.descriptionTooltip.id")}
          place={"right"}
          tip={t("searchFindings.tabEvidence.descriptionTooltip")}
        >
          <Field
            component={FormikTextArea}
            name={getFieldName("description")}
            validate={composeValidators([
              maxDescriptionLength,
              validEvidenceDescription,
              validTextField,
            ])}
          />
        </Tooltip>
      ) : (
        <p>{description}</p>
      )}
      {isRemovable ? (
        <Tooltip
          id={t("searchFindings.tabEvidence.removeTooltip.id")}
          tip={t("searchFindings.tabEvidence.removeTooltip")}
        >
          <Button onClick={onDelete} variant={"secondary"}>
            <FontAwesomeIcon icon={faTrashAlt} />
            &nbsp;{t("searchFindings.tabEvidence.remove")}
          </Button>
        </Tooltip>
      ) : undefined}
    </div>
  );
};

const EvidenceImage: React.FC<IEvidenceImageProps> = (
  props: IEvidenceImageProps
): JSX.Element => {
  const { content, isEditing, description, date, name, onClick } = props;
  const { t } = useTranslation();
  const handleClick = useCallback((): void => {
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
                key={`${name}.img.key`}
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
                <b>{t("searchFindings.tabEvidence.detail")}</b>
              </label>
            </Row>
            <Row>
              {isEditing ? (
                <RenderForm {...props} />
              ) : (
                <React.Fragment>
                  <EvidenceDescription>{description}</EvidenceDescription>
                  {_.isEmpty(date) ? undefined : (
                    <EvidenceDescription>
                      {t("searchFindings.tabEvidence.date")}&nbsp;
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
