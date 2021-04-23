/* eslint-disable @typescript-eslint/prefer-readonly-parameter-types, react/forbid-component-props
  -------
  Readonly utility type does not work on deeply nested types and we need
  className to override default styles from react-bootstrap.
*/
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FieldInputProps, FieldProps } from "formik";
import _ from "lodash";
import React from "react";

import {
  ControlLabel,
  FormGroup,
  InputGroup,
  ValidationError,
} from "styles/styledComponents";
import style from "utils/forms/index.css";

interface IFileInputProps extends FieldProps {
  accept?: string;
  className?: string;
  id?: string;
  input: Omit<FieldInputProps<FileList>, "value"> & { value: FileList };
  onClick: () => void;
}

export const FormikFileInput: React.FC<IFileInputProps> = (
  props: Readonly<IFileInputProps>
): JSX.Element => {
  const { accept, className, id, field, form, onClick } = props;
  const { touched, errors, setFieldValue } = form;
  const fieldTouched = Boolean(touched[field.name]);
  const error = errors[field.name];
  const { name } = field;
  const { value }: { value: FileList } = field;

  function handleFileChange(event: React.FormEvent<HTMLInputElement>): void {
    const { files } = event.currentTarget as HTMLInputElement;
    setFieldValue(name, files);
  }

  return (
    <FormGroup id={id}>
      <InputGroup className={className}>
        <div className={`${style.inputfile} ${style.inputfile_evidence}`} />
        <ControlLabel>
          <span>{_.isEmpty(value) ? "" : value[0].name}</span>
          <input
            accept={accept}
            className={style.inputfileBtn}
            name={name}
            onChange={handleFileChange}
            onClick={onClick}
            type={"file"}
          />
          <strong className={"f7"}>
            <FontAwesomeIcon icon={faSearch} /> {"Explore\u2026"}
          </strong>
        </ControlLabel>
      </InputGroup>
      {fieldTouched && error !== undefined ? (
        <ValidationError id={"validationError"}>{error}</ValidationError>
      ) : undefined}
    </FormGroup>
  );
};
