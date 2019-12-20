import BootstrapSwitchButton from "bootstrap-switch-button-react";
import React, { ReactElement } from "react";
import { Label } from "react-bootstrap";
import { FluidIcon } from "../FluidIcon";
import { default as style } from "./index.css";
import { IHeader } from "./types";

export const statusFormatter: ((value: string) => ReactElement<Label>) =
  (value: string): ReactElement<Label> => {
    let bgColor: string;
    let status: string; status = "";
    switch (value) {
      case "Closed":
      case "Solved":
      case "Active":
        bgColor = "#31c0be";
        break;
      case "Open":
      case "Unsolved":
      case "Inactive":
        bgColor = "#f22";
        break;
      case "Partially closed":
        bgColor = "#ffbf00";
        break;
      case "Submitted":
          bgColor = "#31c0be";
          status = value;
          break;
      case "Rejected":
          bgColor = "#f22";
          status = value;
          break;
      case "Created":
          bgColor = "#ffbf00";
          status = value;
          break;
      default:
        bgColor = "";
        status = "";
    }

    return (
      <Label
        className={style.label}
        style={{backgroundColor: bgColor}}
      >
        {status === "" ? value : status}
      </Label>
    );
};

export const approveFormatter: ((value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader)
=> JSX.Element) =
  (value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader): JSX.Element => {
    const handleApproveFormatter: (() => void) = (): void => {
      if (key.approveFunction !== undefined) {
        key.approveFunction(row);
      }
    };

    return (
      <a onClick={handleApproveFormatter}>
        <FluidIcon icon="verified" width="20px" height="20px" />
      </a>
    );
  };

export const changeFormatter: ((value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader)
=> JSX.Element) =
  (value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader): JSX.Element => {
  const handleOnChange: (() => void) = (): void => {
    if (key.changeFunction !== undefined) {
      key.changeFunction(row);
    }
  };

  return (
    <BootstrapSwitchButton
      onChange={handleOnChange}
      checked={!("state" in row) || row.state !== "Inactive"}
      onstyle="danger"
      onlabel="Active"
      offlabel="Inactive"
      style="btn-block"
    />
    );
  };

export const deleteFormatter: ((value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader)
=> JSX.Element) =
  (value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader): JSX.Element => {
    const handleDeleteFormatter: (() => void) = (): void => {
      if (key.deleteFunction !== undefined) {
        key.deleteFunction(row);
      }
    };

    return (
      <a onClick={handleDeleteFormatter}>
        <FluidIcon icon="delete" width="20px" height="20px" />
      </a>
    );
  };
