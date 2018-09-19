/* tslint:disable jsx-no-multiline-js
 * Disabling this rule is necessary for the sake of readability
 * of the code that renders/hides the component
 */
import PropTypes from "prop-types";
import React from "react";
import { ControlLabel, FormControl, FormGroup, Glyphicon } from "react-bootstrap";
import style from "./index.css";
/**
 * File Input properties
 */
interface IFileInputProps {
  icon: string;
  id: string;
  type: string;
  visible: boolean;
}

/**
 * File Input
 */
const fileInput: React.StatelessComponent<IFileInputProps> =
  (props: IFileInputProps): JSX.Element => (
    <React.StrictMode>
      { props.visible
        ? <FormGroup controlId={props.id} className={style.text_center}>
            <FormControl
              className={`${style.inputfile} ${style.inputfile_evidence}`}
              type="file"
              accept={props.type}
              name={`${props.id}[]`}
            />
            <ControlLabel>
              <span />
              <strong>
                <Glyphicon glyph={props.icon}/> Choose a file&hellip;
              </strong>
            </ControlLabel>
          </FormGroup>
        : undefined
      }
    </React.StrictMode>
);
/**
 *  File Input's propTypes Definition
 */
fileInput.propTypes = {
  icon: PropTypes.string,
  id: PropTypes.string,
  type: PropTypes.string,
  visible: PropTypes.bool.isRequired,
};

fileInput.defaultProps = {
  icon: "",
  id: "",
  type: "",
  visible: false,
};

export = fileInput;
