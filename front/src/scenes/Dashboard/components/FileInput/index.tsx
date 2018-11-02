/* tslint:disable jsx-no-multiline-js jsx-no-lambda no-any
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of readability
 * of the code that renders/hides the component
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 */
import PropTypes from "prop-types";
import React, { ComponentType } from "react";
import { ControlLabel, FormControl, FormGroup, Glyphicon } from "react-bootstrap";
import { Reducer } from "redux";
import { StateType } from "typesafe-actions";
import store from "../../../../store/index";
import reduxWrapper from "../../../../utils/reduxWrapper";
import * as actions from "../../actions";
import style from "./index.css";
/**
 * File Input properties
 */
export interface IFileInputProps {
  fileName: string;
  icon: string;
  id: string;
  target?: string;
  type: string;
  visible: boolean;
}

/**
 * File Input
 */

const mapStateToProps: ((arg1: StateType<Reducer>) => IFileInputProps) =
  (state: StateType<Reducer>): IFileInputProps => ({
    ...state,
    fileName: state.dashboard.fileInput.name,
  });

export const fileInputComponent: React.StatelessComponent<IFileInputProps> =
  (props: IFileInputProps): JSX.Element => (
    <React.StrictMode>
      { props.visible
        ? <FormGroup controlId={props.id} className={style.text_center}>
            <FormControl
              target={props.target}
              className={`${style.inputfile} ${style.inputfile_evidence}`}
              type="file"
              accept={props.type}
              name={`${props.id}[]`}
              onChange={(evt: React.FormEvent<FormControl>): void => {
                              store.dispatch(actions.addFileName((evt.target as HTMLInputElement).files));
              }}
            />
            <ControlLabel>
              <span>{props.fileName}</span>
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
fileInputComponent.propTypes = {
  fileName: PropTypes.string,
  icon: PropTypes.string,
  id: PropTypes.string,
  type: PropTypes.string,
  visible: PropTypes.bool.isRequired,
};

fileInputComponent.defaultProps = {
  fileName: "",
  icon: "",
  id: "",
  type: "",
  visible: false,
};

export const fileInput: ComponentType<IFileInputProps> = reduxWrapper
(
  fileInputComponent,
  mapStateToProps,
);
