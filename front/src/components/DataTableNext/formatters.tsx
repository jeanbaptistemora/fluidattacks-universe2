import BootstrapSwitchButton from "bootstrap-switch-button-react";
import React, { ReactElement } from "react";
import { Col, Label, Row } from "react-bootstrap";
import translate from "../../utils/translations/translate";
import { FluidIcon } from "../FluidIcon";
import { default as style } from "./index.css";
import { IHeader } from "./types";

export const statusFormatter: ((value: string) => ReactElement<Label>) =
  (value: string): ReactElement<Label> => {
    let bgColor: string;
    let status: string; status = "";
    switch (value) {
      // Green
      case "Active":
      case "Closed":
      case "Solved":
      case "Submitted":
      case "Success":
          bgColor = "#00D444";
          status = value;
          break;
      // Orange
      case "Created":
      case "Partially closed":
          bgColor = "#FFBF00";
          status = value;
          break;
      // Red
      case "Failed":
      case "Inactive":
      case "Open":
      case "Rejected":
      case "Unsolved":
          bgColor = "#FF2222";
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

export const limitFormatter: ((value: string) => JSX.Element) = (value: string): JSX.Element => {
  const valueArray: string[] = value.split(",")
    .map((element: string) => element.trim());
  const newValue: string = valueArray.slice(0, 15)
    .join(", ");

  const renderMore: (() => JSX.Element | undefined) = (): JSX.Element | undefined => {
    if (valueArray.length > 15) {
      return (
        <Col sm={12} className={style.limitFormatter}>
          {translate.t("dataTableNext.more")}
        </Col>
      );
    }
  };

  return(
    <Row className={style.limitFormatter}>
      <Col sm={12} className={style.limitFormatter}>
        <p className={style.limitFormatter}>{newValue}</p>
      </Col>
      {renderMore()}
    </Row>
  );
};
export const changeVulnStateFormatter: ((value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader)
  => JSX.Element) = (value: string, row: { [key: string]: string }, rowIndex: number, key: IHeader): JSX.Element => {
    const handleOnChange: (() => void) = (): void => {
      if (key.changeFunction !== undefined) {
        key.changeFunction(row);
      }
    };

    return (
      <BootstrapSwitchButton
        onChange={handleOnChange}
        checked={!("currentState" in row) || row.currentState !== "closed"}
        onstyle="danger"
        onlabel="open"
        offlabel="closed"
        style="btn-block"
      />
    );
  };
