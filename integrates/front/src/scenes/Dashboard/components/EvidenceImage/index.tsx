/* eslint-disable jsx-a11y/click-events-have-key-events, react/jsx-props-no-spreading, react/no-multi-comp */
import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FieldValidator } from "formik";
import { Field, useField, useFormikContext } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import { DisplayImage } from "./DisplayImage";
import { DescriptionContainer, ImageContainer } from "./styles";

import { Button } from "components/Button/index";
import { Editable, TextArea } from "components/Input";
import { Tooltip } from "components/Tooltip";
import type { IEvidenceItem } from "scenes/Dashboard/containers/Finding-Content/EvidenceView/types";
import { Col33, EvidenceDescription, Row } from "styles/styledComponents";
import { FormikFileInput } from "utils/forms/fields";
import {
  composeValidators,
  getFileNameExtension,
  isValidEvidenceDescription,
  maxLength,
  validTextField,
} from "utils/validations";

interface IEvidenceImageProps {
  acceptedMimes?: string;
  content: string;
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

const MAX_DESCRIPTION_LENGTH: number = 5000;
const maxDescriptionLength: ConfigurableValidator = maxLength(
  MAX_DESCRIPTION_LENGTH
);

const RenderForm: React.FC<Readonly<IEvidenceImageProps>> = ({
  acceptedMimes,
  shouldPreview,
  shouldPreviewValidation,
  description,
  isDescriptionEditable,
  isRemovable = false,
  name,
  onDelete,
  validate,
}): JSX.Element => {
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
      <Editable
        currentValue={description}
        isEditing={isDescriptionEditable}
        label={""}
      >
        <TextArea
          label={"Description"}
          name={getFieldName("description")}
          tooltip={t("searchFindings.tabEvidence.descriptionTooltip")}
          validate={composeValidators([
            maxDescriptionLength,
            validEvidenceDescription,
            validTextField,
          ])}
        />
      </Editable>
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

const EvidenceImage: React.FC<Readonly<IEvidenceImageProps>> = (
  props
): JSX.Element => {
  const { content, isEditing, description, date, name, onClick } = props;
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <Col33>
        <div>
          <ImageContainer>
            <DisplayImage
              content={content}
              extension={getFileNameExtension(content)}
              name={name}
              onClick={onClick}
            />
          </ImageContainer>
          <DescriptionContainer>
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
          </DescriptionContainer>
        </div>
      </Col33>
    </React.StrictMode>
  );
};

export { EvidenceImage };
