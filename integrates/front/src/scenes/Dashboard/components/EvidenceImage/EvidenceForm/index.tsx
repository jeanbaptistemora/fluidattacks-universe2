import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useField } from "formik";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import type { IEvidenceImageProps } from "..";
import { DisplayImage } from "../DisplayImage";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Editable, InputFile, TextArea } from "components/Input";
import { Tooltip } from "components/Tooltip";
import {
  composeValidators,
  getFileNameExtension,
  isValidEvidenceDescription,
  maxLength,
  validTextField,
} from "utils/validations";

const MAX_DESCRIPTION_LENGTH = 5000;
const maxDescriptionLength = maxLength(MAX_DESCRIPTION_LENGTH);

const EvidenceForm: React.FC<Readonly<IEvidenceImageProps>> = ({
  acceptedMimes,
  content,
  description,
  isDescriptionEditable,
  isRemovable = false,
  name,
  onDelete,
  validate,
}): JSX.Element => {
  const { t } = useTranslation();

  const [inputProps, , helpers] = useField(`${name}.file`);
  const validEvidenceDescription = isValidEvidenceDescription(
    content,
    inputProps.value
  );
  const [preview, setPreview] = useState<File | undefined>(undefined);
  const shouldRenderPreview = content !== "file";

  return (
    <div>
      <ConfirmDialog
        message={
          <React.Fragment>
            <label>
              {t("searchFindings.tabEvidence.fields.modal.message")}
            </label>
            {preview ? (
              <DisplayImage
                content={URL.createObjectURL(preview)}
                extension={getFileNameExtension(preview.name)}
                name={name}
              />
            ) : undefined}
          </React.Fragment>
        }
        title={t("searchFindings.tabEvidence.fields.modal.title")}
      >
        {(callbacks): React.ReactNode => {
          function handleClick(
            event: React.ChangeEvent<HTMLInputElement>
          ): void {
            const files = event.target.value as unknown as FileList | undefined;

            if (files) {
              setPreview(files[0]);
              callbacks(
                (): void => {
                  helpers.setTouched(true);
                },
                (): void => {
                  helpers.setValue(undefined);
                }
              );
            }
          }

          return (
            <InputFile
              accept={acceptedMimes}
              id={name}
              name={`${name}.file`}
              onChange={shouldRenderPreview ? handleClick : undefined}
              validate={validate}
            />
          );
        }}
      </ConfirmDialog>
      <Editable
        currentValue={description}
        isEditing={isDescriptionEditable}
        label={""}
      >
        <TextArea
          label={"Description"}
          name={`${name}.description`}
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

export { EvidenceForm };
