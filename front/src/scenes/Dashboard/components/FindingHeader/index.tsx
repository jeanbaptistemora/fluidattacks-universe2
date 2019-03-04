import _ from "lodash";
import React from "react";
import { Col, Glyphicon, Row } from "react-bootstrap";
import CircularProgressbar, { ProgressbarClasses } from "react-circular-progressbar";
import { default as calendarIcon } from "../../../../resources/calendar.svg";
import { default as vulnerabilitiesIcon } from "../../../../resources/vulnerabilities.svg";
import translate from "../../../../utils/translations/translate";
import style from "./index.css";

interface IFindingHeaderProps {
  openVulns: number;
  reportDate: string;
  severity: number;
  status: "Abierto" | "Cerrado";
}

const severityConfigs: { [level: string]: { color: string; text: string } } = {
  HIGH: { color: "#FF1122", text: translate.t("search_findings.high_severity") },
  LOW: { color: "#FFBF00", text: translate.t("search_findings.low_severity") },
  MED: { color: "#FF7722", text: translate.t("search_findings.medium_severity") },
};

const statusConfigs: { [level: string]: { color: string; icon: string; text: string } } = {
  Abierto: { color: "#810404CF", icon: "remove-sign", text: translate.t("search_findings.status.open") },
  Cerrado: { color: "#108104CF", icon: "ok-sign", text: translate.t("search_findings.status.closed") },
  Default: { color: "", icon: "", text: "" },
};

const findingHeader: React.SFC<IFindingHeaderProps> = (props: IFindingHeaderProps): JSX.Element => {
  const severityLevel: "HIGH" | "MED" | "LOW" = props.severity > 6.9 ? "HIGH" : props.severity > 3.9 ? "MED" : "LOW";
  const { color: severityColor, text: severityText } = severityConfigs[severityLevel];
  const { color: statusColor, icon: statusIcon, text: statusText } =
    statusConfigs[_.isUndefined(props.status) ? "Default" : props.status];
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
              <CircularProgressbar
                percentage={props.severity / 10 * 100}
                text={`${props.severity}`}
                initialAnimation={true}
                styles={{ text: { fill: severityColor }, path: { stroke: severityColor } }}
                classes={severityStyles}
              />
              <p>{translate.t("search_findings.severityLabel")}</p>
              <p className={style.highlightedIndicator}><b>{severityText}</b></p>
            </Row>
          </Col>
          <Col md={3}>
            <Row>
              <Glyphicon
                glyph={statusIcon}
                bsClass="glyphicon"
                className={style.statusIcon}
                style={{ color: statusColor }}
              />
              <p>{translate.t("search_findings.statusLabel")}</p>
              <p className={style.highlightedIndicator}><b>{statusText}</b></p>
            </Row>
          </Col>
          <Col md={3}>
            <Row>
              <Col md={3}><img src={vulnerabilitiesIcon} width={65} height={65} /></Col>
              <Col md={9}>
                <p>{translate.t("search_findings.openVulnsLabel")}</p>
                <p className={style.highlightedIndicator}>{props.openVulns}</p>
              </Col>
            </Row>
          </Col>
          <Col md={3}>
            <Row>
              <Col md={3}><img src={calendarIcon} width={65} height={65} /></Col>
              <Col md={9}>
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

findingHeader.defaultProps = { severity: 0 };

export { findingHeader as FindingHeader };
