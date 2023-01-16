/* eslint-disable react/forbid-component-props
  ----
  We need className to override default styles from react-bootstrap.
*/
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FieldInputProps, FieldProps, FieldValidator } from "formik";
import { ErrorMessage } from "formik";
import _ from "lodash";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { ConfirmDialog } from "./modal";

import { Alert } from "components/Alert";
import { Label } from "components/Input";
import { ControlLabel, FormGroup, InputGroup } from "styles/styledComponents";
import { ValidationError } from "utils/forms/fields/styles";
import style from "utils/forms/index.css";
import { getFileNameExtension } from "utils/validations";

interface IFileInputProps extends FieldProps {
  accept?: string;
  confirmTitle?: string;
  confirmMessage?: string;
  className?: string;
  id?: string;
  input: Omit<FieldInputProps<FileList>, "value"> & { value: FileList };
  multiple?: boolean;
  onClick: () => void;
  shouldPreview?: boolean;
  shouldPreviewValidation?: FieldValidator[];
}

export const FormikFileInput: React.FC<IFileInputProps> = (
  props: Readonly<IFileInputProps>
): JSX.Element => {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [alert, setAlert] = useState<string>("");
  const [isAlertOpen, setIsAlertOpen] = useState<boolean>(false);
  const [imgUrl, setImgUrl] = useState<string>("#");
  const [imgName, setImgName] = useState<string>("");
  const {
    accept,
    className,
    id,
    field,
    form,
    multiple = false,
    onClick,
    shouldPreview = false,
    shouldPreviewValidation = undefined,
  } = props;
  const { setFieldValue } = form;
  const { name } = field;
  const { value }: { value: FileList } = field;

  function handleFileChange(event: React.FormEvent<HTMLInputElement>): void {
    const { files } = event.currentTarget as HTMLInputElement;
    setFieldValue(name, files);
  }
  function handlePreviewChange(files: FileList | null): void {
    if (shouldPreviewValidation !== undefined) {
      if (
        shouldPreviewValidation.every((validator: FieldValidator): boolean => {
          return validator(files) === undefined;
        })
      ) {
        setAlert("");
        if (files !== null) {
          setIsAlertOpen(false);
          const url: string = URL.createObjectURL(files[0]);
          setImgUrl(url);
          setImgName(files[0].name);
        }
      } else {
        setAlert(
          shouldPreviewValidation.reduce(
            (previousValue: string, validator: FieldValidator): string => {
              const validatorValue = validator(files);

              return validatorValue === undefined ||
                typeof validatorValue !== "string"
                ? previousValue
                : `${previousValue} ${validatorValue as unknown as string}.`;
            },
            ""
          )
        );
        setIsAlertOpen(true);
        setImgUrl("#");
        setImgName("");
      }
    }
  }

  return (
    <ConfirmDialog
      disable={isAlertOpen}
      isOpen={isOpen}
      message={
        <React.Fragment>
          <Label>{t("searchFindings.tabEvidence.fields.modal.message")}</Label>
          <div>
            {getFileNameExtension(imgName) === "webm" ? (
              <video controls={true} height={600} muted={true} width={600}>
                <source src={imgUrl} type={"video/webm"} />
              </video>
            ) : (
              <img
                alt={""}
                height={600}
                key={`${name}.img.key`}
                src={imgUrl}
                width={600}
              />
            )}
          </div>
          <div style={{ width: "650px" }}>
            <Alert show={isAlertOpen}>
              <React.Fragment>
                {t("searchFindings.tabEvidence.fields.modal.error")}
                <p className={"pa0 ma0"}>{t(alert)}</p>
              </React.Fragment>
            </Alert>
          </div>
        </React.Fragment>
      }
      title={t("searchFindings.tabEvidence.fields.modal.title")}
    >
      {(callbacks): React.ReactNode => {
        function handleClick(event: React.FormEvent<HTMLInputElement>): void {
          setIsOpen(true);
          const { files } = event.currentTarget as HTMLInputElement;
          handlePreviewChange(files);
          callbacks(
            (): void => {
              setFieldValue(name, files);
              setIsOpen(false);
            },
            (): void => {
              setIsOpen(false);
            }
          );
        }

        return (
          <FormGroup id={id}>
            <InputGroup className={className}>
              <div
                className={`${style.inputfile} ${style.inputfile_evidence}`}
              />
              <ControlLabel>
                <span>{_.isEmpty(value) ? "" : value[0].name}</span>
                <input
                  accept={accept}
                  className={style.inputfileBtn}
                  data-testid={name}
                  multiple={multiple}
                  name={name}
                  onChange={
                    shouldPreview && !multiple ? handleClick : handleFileChange
                  }
                  onClick={onClick}
                  type={"file"}
                />
                <strong className={"f7"}>
                  <FontAwesomeIcon icon={faSearch} /> {"Explore\u2026"}
                </strong>
              </ControlLabel>
            </InputGroup>
            <ValidationError>
              <ErrorMessage name={name} />
            </ValidationError>
          </FormGroup>
        );
      }}
    </ConfirmDialog>
  );
};
