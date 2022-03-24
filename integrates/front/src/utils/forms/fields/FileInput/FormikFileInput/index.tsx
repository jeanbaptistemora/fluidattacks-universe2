/* eslint-disable react/forbid-component-props
  ----
  We need className to override default styles from react-bootstrap.
*/
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FieldInputProps, FieldProps } from "formik";
import { ErrorMessage } from "formik";
import _ from "lodash";
import React from "react";

import { ControlLabel, FormGroup, InputGroup } from "styles/styledComponents";
import { ValidationError } from "utils/forms/fields/styles";
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
  const { setFieldValue } = form;
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
            data-testid={name}
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
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </FormGroup>
  );
};
