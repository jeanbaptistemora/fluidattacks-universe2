/* eslint-disable @typescript-eslint/prefer-readonly-parameter-types, react/forbid-component-props
  -------
  Readonly utility type does not work on deeply nested types and we need
  className to override default styles from react-bootstrap.
*/
import { Glyphicon } from "react-bootstrap";
import React from "react";
import _ from "lodash";
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
  input: { value: FileList } & Omit<WrappedFieldInputProps, "value">;
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
          <strong>
            <Glyphicon glyph={"search"} /> {"Explore"}&hellip;
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
