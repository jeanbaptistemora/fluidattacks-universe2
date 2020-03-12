/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of readability
 * of the code that renders/hides the component
 */
import _ from "lodash";
import React, { useState } from "react";
import { ControlLabel, FormControl, FormGroup, Glyphicon, InputGroup, Row } from "react-bootstrap";
import translate from "../../../../utils/translations/translate";
import { default as style } from "./index.css";
/**
 * File Input properties
 */
export interface IFileInputProps {
  fileSize?: number;
  icon: string;
  id: string;
  target?: string;
  type: string;
  visible: boolean;
}

export const fileInputComponent: React.FunctionComponent<IFileInputProps> =
  (props: IFileInputProps): JSX.Element => {
    const [fileName, setFileName] = useState("");
    const handleFileNameChange: (evt: React.FormEvent<FormControl>) => void =
      (evt: React.FormEvent<FormControl>): void => {
        const target: HTMLInputElement = evt.target as HTMLInputElement;
        if (!_.isNil(target.files) && target.files.length > 0) {
          setFileName(target.files[0].name);
        } else {
          setFileName("");
        }
      };

    return (
    <React.StrictMode>
      { props.visible
        ? <FormGroup controlId={props.id} className={style.text_center}>
            <InputGroup>
              <Row>
                <FormControl
                  target={props.target}
                  className={`${style.inputfile} ${style.inputfile_evidence}`}
                  type="file"
                  accept={props.type}
                  name={`${props.id}[]`}
                  onChange={handleFileNameChange}
                />
                <ControlLabel>
                  <span>{fileName}</span>
                  <strong>
                    <Glyphicon glyph={props.icon}/>&nbsp;Explore&hellip;
                  </strong>
                </ControlLabel>
              </Row>
              { !_.isUndefined(props.fileSize) ?
                <Row>
                  <label style={{ color: "#f22" }}>* </label>
                  {translate.t("validations.file_size", { count: props.fileSize })}
                </Row>
                : undefined
              }
            </InputGroup>
          </FormGroup>
        : undefined
      }
    </React.StrictMode>
    );
  };

export { fileInputComponent as FileInput};
