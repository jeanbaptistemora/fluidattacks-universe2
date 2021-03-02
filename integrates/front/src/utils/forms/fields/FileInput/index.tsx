/* eslint-disable @typescript-eslint/prefer-readonly-parameter-types, react/forbid-component-props
  -------
  Readonly utility type does not work on deeply nested types and we need
  className to override default styles from react-bootstrap.
*/
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import _ from "lodash";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import style from "utils/forms/index.css";
import {
  ControlLabel,
  FormGroup,
  InputGroup,
  ValidationError,
} from "styles/styledComponents";
import type { WrappedFieldInputProps, WrappedFieldProps } from "redux-form";

interface IFileInputProps extends WrappedFieldProps {
  accept?: string;
  className?: string;
  id?: string;
  input: Omit<WrappedFieldInputProps, "value"> & { value: FileList };
  name?: string;
  onClick: () => void;
}

export const FileInput: React.FC<IFileInputProps> = (
  props: Readonly<IFileInputProps>
): JSX.Element => {
  const { accept, className, id, input, name, meta, onClick } = props;
  const { onChange, value } = input;
  const { touched, error } = meta;

  function handleFileChange(event: React.FormEvent<HTMLInputElement>): void {
    const files: FileList | null = (event.target as HTMLInputElement).files;
    onChange(_.isEmpty(files) ? [] : (files as FileList));
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
      {touched && !_.isUndefined(error) && (
        <ValidationError id={"validationError"}>
          {error as string}
        </ValidationError>
      )}
    </FormGroup>
  );
};
