/* eslint-disable @typescript-eslint/prefer-readonly-parameter-types, react/forbid-component-props
  -------
  Readonly utility type does not work on deeply nested types and we need
  className to override default styles from react-bootstrap.
*/
import React from "react";
import _ from "lodash";
import style from "utils/forms/index.css";
import {
  ControlLabel,
  FormControl,
  FormControlProps,
  FormGroup,
  Glyphicon,
  HelpBlock,
  InputGroup,
} from "react-bootstrap";
import { WrappedFieldInputProps, WrappedFieldProps } from "redux-form";

interface IFileInputProps extends WrappedFieldProps, FormControlProps {
  input: { value: FileList } & Omit<WrappedFieldInputProps, "value">;
}

export const FileInput: React.FC<IFileInputProps> = (
  props: Readonly<IFileInputProps>
): JSX.Element => {
  const { accept, id, input, name, meta, onClick, target } = props;
  const { onChange, value } = input;
  const { touched, error } = meta;

  function handleFileChange(event: React.FormEvent<FormControl>): void {
    const files: FileList | null = (event.target as HTMLInputElement).files;
    onChange(_.isEmpty(files) ? [] : (files as FileList));
  }

  return (
    <FormGroup controlId={id}>
      <InputGroup>
        <FormControl
          accept={accept}
          className={`${style.inputfile} ${style.inputfile_evidence}`}
          name={name}
          onChange={handleFileChange}
          onClick={onClick}
          target={target}
          type={"file"}
        />
        <ControlLabel>
          <span>{_.isEmpty(value) ? "" : value[0].name}</span>
          <strong>
            <Glyphicon glyph={"search"} /> {"Explore"}&hellip;
          </strong>
        </ControlLabel>
      </InputGroup>
      {touched && !_.isUndefined(error) && (
        <HelpBlock className={style.validationError} id={"validationError"}>
          {error as string}
        </HelpBlock>
      )}
    </FormGroup>
  );
};
