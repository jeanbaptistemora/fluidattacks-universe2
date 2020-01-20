import React from "react";
import { Col, Row } from "react-bootstrap";
import CircularProgressbar, { ProgressbarClasses } from "react-circular-progressbar";
import { default as calendarIcon } from "../../../../resources/calendar.svg";
import { default as defaultIcon } from "../../../../resources/default_finding_state.svg";
import { default as failIcon } from "../../../../resources/fail.svg";
import { default as okIcon } from "../../../../resources/ok.svg";
import { default as vulnerabilitiesIcon } from "../../../../resources/vulnerabilities.svg";
import translate from "../../../../utils/translations/translate";
import { default as style } from "./index.css";

interface IFindingHeaderProps {
  openVulns: number;
  reportDate: string;
  severity: number;
  status: "open" | "closed" | "default";
}

const severityConfigs: { [level: string]: { color: string; text: string } } = {
  CRITICAL: { color: "#96030D", text: translate.t("search_findings.critical_severity") },
  HIGH: { color: "#FF1122", text: translate.t("search_findings.high_severity") },
  LOW: { color: "#FFBF00", text: translate.t("search_findings.low_severity") },
  MED: { color: "#FF7722", text: translate.t("search_findings.medium_severity") },
  NONE: { color: "#FF7722", text: translate.t("search_findings.none_severity") },
};

const statusConfigs: { [level: string]: { icon: string; text: string } } = {
  closed: { icon: okIcon, text: translate.t("search_findings.status.closed") },
  default: { icon: defaultIcon, text: "" },
  open: { icon: failIcon, text: translate.t("search_findings.status.open") },
};

const findingHeader: React.FC<IFindingHeaderProps> = (props: IFindingHeaderProps): JSX.Element => {
  const severityLevel: "CRITICAL" | "HIGH" | "MED" | "LOW" | "NONE" =
    props.severity >= 9 ? "CRITICAL"
      : props.severity > 6.9 ? "HIGH"
        : props.severity > 3.9 ? "MED"
          : props.severity >= 0.1 ? "LOW"
            : "NONE";
  const { color: severityColor, text: severityText } = severityConfigs[severityLevel];
  const { icon: statusIcon, text: statusText } = statusConfigs[props.status];
  const severityStyles: ProgressbarClasses = {
    background: style.severityCircleBg,
    path: style.severityCirclePath,
    root: style.severityCircle,
    text: style.severityCircleText,
    trail: style.severityCircleTrail,
  };

  return (
    <React.StrictMode>
      <Row className={style.container}>
        <Col md={12}>
          <Col md={3}>
            <Row>
              <Col md={3} sm={6} xs={6} className={style.headerIcon}>
                <CircularProgressbar
                  percentage={props.severity / 10 * 100}
                  text={`${props.severity}`}
                  initialAnimation={true}
                  styles={{ text: { fill: severityColor }, path: { stroke: severityColor } }}
                  classes={severityStyles}
                />
              </Col>
              <Col md={9} sm={6} xs={6}>
                <p>{translate.t("search_findings.severityLabel")}</p>
                <p className={style.highlightedIndicator}><b>{severityText}</b></p>
              </Col>
            </Row>
          </Col>
          <Col md={3}>
            <Row>
              <Col md={3} sm={6} xs={6} className={style.headerIcon}>
                <img src={statusIcon} width={45} height={45} />
              </Col>
              <Col md={9} sm={6} xs={6}>
                <p>{translate.t("search_findings.statusLabel")}</p>
                <p className={style.highlightedIndicator}><b>{statusText}</b></p>
              </Col>
            </Row>
          </Col>
          <Col md={3}>
            <Row>
              <Col md={3} sm={6} xs={6} className={style.headerIcon}>
                <img src={vulnerabilitiesIcon} width={45} height={45} />
              </Col>
              <Col md={9} sm={6} xs={6}>
                <p>{translate.t("search_findings.openVulnsLabel")}</p>
                <p className={style.highlightedIndicator}>{props.openVulns}</p>
              </Col>
            </Row>
          </Col>
          <Col md={3}>
            <Row>
              <Col md={3} sm={6} xs={6} className={style.headerIcon}>
                <img src={calendarIcon} width={40} height={40} />
              </Col>
              <Col md={9} sm={6} xs={6}>
                <p>{translate.t("search_findings.reportDateLabel")}</p>
                <p className={style.highlightedIndicator}>{props.reportDate}</p>
              </Col>
            </Row>
          </Col>
        </Col>
      </Row>
    </React.StrictMode>
  );
};

export { findingHeader as FindingHeader };
