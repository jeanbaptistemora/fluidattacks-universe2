/* eslint-disable fp/no-mutating-methods */
import React from "react";
import { useTranslation } from "react-i18next";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { SeverityTile, severityImages } from "./tile";

import type { ISeverityAttr } from "../types";
import {
  attackComplexityBgColor,
  attackComplexityOptions,
  attackVectorBgColor,
  attackVectorOptions,
  availabilityImpactBgColor,
  availabilityImpactOptions,
  castPrivileges,
  confidentialityImpactBgColor,
  confidentialityImpactOptions,
  exploitabilityBgColor,
  exploitabilityOptions,
  integrityImpactBgColor,
  integrityImpactOptions,
  privilegesRequiredBgColor,
  remediationLevelBgColor,
  remediationLevelOptions,
  reportConfidenceBgColor,
  reportConfidenceOptions,
  severityScopeBgColor,
  severityScopeOptions,
  userInteractionBgColor,
  userInteractionOptions,
} from "../utils";
import { TooltipWrapper } from "components/TooltipWrapper";

const Row: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "w-100-m w-25-ns pa1",
})``;

const Col: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "pa1 w-100 mb3-l mb2-m mb1-ns",
})``;

const FlexCol: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "flex flex-column items-center",
})``;

export const SeverityContent: React.FC<ISeverityAttr["finding"]["severity"]> =
  ({
    attackVector,
    attackComplexity,
    availabilityImpact,
    confidentialityImpact,
    exploitability,
    integrityImpact,
    privilegesRequired,
    remediationLevel,
    reportConfidence,
    severityScope,
    userInteraction,
  }: ISeverityAttr["finding"]["severity"]): JSX.Element => {
    const { t } = useTranslation();

    function getPrivilegesRequiredColor(value: string): string {
      if (t(castPrivileges(severityScope)[value]) === "None") {
        return "bg-dark-red";
      } else if (t(castPrivileges(severityScope)[value]) === "Low") {
        return "bg-orange";
      }

      return "bg-lbl-yellow";
    }

    function getTooltips(
      metricOptions: Record<string, string>,
      metricValue: string,
      bgColor: Record<string, string>
    ): string {
      const ind = 3;

      return (
        "<table aria-label='" +
        `${metricOptions[metricValue].split(".")[2]}` +
        "Table'><tr><td colspan='2'>" +
        `${t(
          `${metricOptions[metricValue].split(".").slice(0, ind).join(".")}` +
            ".tooltip"
        )}` +
        "</td></tr>" +
        `${Object.keys(metricOptions)
          .sort(
            (last, current): number => parseFloat(current) - parseFloat(last)
          )
          .map(function tooltipsRow(key): string {
            return (
              `${
                metricOptions[key] === metricOptions[metricValue]
                  ? `<tr class='${bgColor[key]} black'><td style='width: 20%'>`
                  : `<tr><td style='width: 20%' class='${bgColor[key]} black'>`
              }` +
              "<img src='" +
              `${
                severityImages[
                  metricOptions[key].split(".")[2] +
                    t(metricOptions[key]).split(" ")[0]
                ]
              }` +
              "'></td><td style='padding: 10px; text-align: left;'>" +
              `${t(metricOptions[key].replace(/label/u, "tooltip"))}` +
              "</td></tr>"
            );
          })
          .join("\n")}` +
        "</table>"
      );
    }

    return (
      <React.StrictMode>
        <div className={"flex flex-wrap items-center h-100 w-100"}>
          <Row>
            <FlexCol>
              <Col>
                <TooltipWrapper
                  id={"userInteractionTooltip"}
                  message={getTooltips(
                    userInteractionOptions,
                    userInteraction,
                    userInteractionBgColor
                  )}
                >
                  <SeverityTile
                    color={userInteractionBgColor[userInteraction]}
                    name={"userInteraction"}
                    value={userInteraction}
                    valueText={t(userInteractionOptions[userInteraction])}
                  />
                </TooltipWrapper>
              </Col>
              <Col>
                <TooltipWrapper
                  id={"privilegesRequiredTooltip"}
                  message={getTooltips(
                    castPrivileges(severityScope),
                    privilegesRequired,
                    privilegesRequiredBgColor
                  )}
                >
                  <SeverityTile
                    color={getPrivilegesRequiredColor(privilegesRequired)}
                    name={"privilegesRequired"}
                    value={privilegesRequired}
                    valueText={t(
                      castPrivileges(severityScope)[privilegesRequired]
                    )}
                  />
                </TooltipWrapper>
              </Col>
            </FlexCol>
          </Row>
          <Row>
            <FlexCol>
              <Col>
                <TooltipWrapper
                  id={"attackVectorTooltip"}
                  message={getTooltips(
                    attackVectorOptions,
                    attackVector,
                    attackVectorBgColor
                  )}
                >
                  <SeverityTile
                    color={attackVectorBgColor[attackVector]}
                    name={"attackVector"}
                    value={attackVector}
                    valueText={t(attackVectorOptions[attackVector])}
                  />
                </TooltipWrapper>
              </Col>
              <Col>
                <TooltipWrapper
                  id={"attackComplexityTooltip"}
                  message={getTooltips(
                    attackComplexityOptions,
                    attackComplexity,
                    attackComplexityBgColor
                  )}
                >
                  <SeverityTile
                    color={attackComplexityBgColor[attackComplexity]}
                    name={"attackComplexity"}
                    value={attackComplexity}
                    valueText={t(attackComplexityOptions[attackComplexity])}
                  />
                </TooltipWrapper>
              </Col>
              <Col>
                <TooltipWrapper
                  id={"exploitabilityTooltip"}
                  message={getTooltips(
                    exploitabilityOptions,
                    exploitability,
                    exploitabilityBgColor
                  )}
                >
                  <SeverityTile
                    color={exploitabilityBgColor[exploitability]}
                    name={"exploitability"}
                    value={exploitability}
                    valueText={t(exploitabilityOptions[exploitability])}
                  />
                </TooltipWrapper>
              </Col>
              <Col>
                <TooltipWrapper
                  id={"severityScopeTooltip"}
                  message={getTooltips(
                    severityScopeOptions,
                    severityScope,
                    severityScopeBgColor
                  )}
                >
                  <SeverityTile
                    color={severityScopeBgColor[severityScope]}
                    name={"severityScope"}
                    value={severityScope}
                    valueText={t(severityScopeOptions[severityScope])}
                  />
                </TooltipWrapper>
              </Col>
            </FlexCol>
          </Row>
          <Row>
            <FlexCol>
              <Col>
                <TooltipWrapper
                  id={"availabilityImpactTooltip"}
                  message={getTooltips(
                    availabilityImpactOptions,
                    availabilityImpact,
                    availabilityImpactBgColor
                  )}
                >
                  <SeverityTile
                    color={availabilityImpactBgColor[availabilityImpact]}
                    name={"availabilityImpact"}
                    value={availabilityImpact}
                    valueText={t(availabilityImpactOptions[availabilityImpact])}
                  />
                </TooltipWrapper>
              </Col>
              <Col>
                <TooltipWrapper
                  id={"integrityImpactTooltip"}
                  message={getTooltips(
                    integrityImpactOptions,
                    integrityImpact,
                    integrityImpactBgColor
                  )}
                >
                  <SeverityTile
                    color={integrityImpactBgColor[integrityImpact]}
                    name={"integrityImpact"}
                    value={integrityImpact}
                    valueText={t(integrityImpactOptions[integrityImpact])}
                  />
                </TooltipWrapper>
              </Col>
              <Col>
                <TooltipWrapper
                  id={"confidentialityImpactTooltip"}
                  message={getTooltips(
                    confidentialityImpactOptions,
                    confidentialityImpact,
                    confidentialityImpactBgColor
                  )}
                >
                  <SeverityTile
                    color={confidentialityImpactBgColor[confidentialityImpact]}
                    name={"confidentialityImpact"}
                    value={confidentialityImpact}
                    valueText={t(
                      confidentialityImpactOptions[confidentialityImpact]
                    )}
                  />
                </TooltipWrapper>
              </Col>
            </FlexCol>
          </Row>
          <Row>
            <FlexCol>
              <Col>
                <TooltipWrapper
                  id={"remediationLevelTooltip"}
                  message={getTooltips(
                    remediationLevelOptions,
                    remediationLevel,
                    remediationLevelBgColor
                  )}
                >
                  <SeverityTile
                    color={remediationLevelBgColor[remediationLevel]}
                    name={"remediationLevel"}
                    value={remediationLevel}
                    valueText={t(remediationLevelOptions[remediationLevel])}
                  />
                </TooltipWrapper>
              </Col>
              <Col>
                <TooltipWrapper
                  id={"reportConfidenceTooltip"}
                  message={getTooltips(
                    reportConfidenceOptions,
                    reportConfidence,
                    reportConfidenceBgColor
                  )}
                >
                  <SeverityTile
                    color={reportConfidenceBgColor[reportConfidence]}
                    name={"reportConfidence"}
                    value={reportConfidence}
                    valueText={t(reportConfidenceOptions[reportConfidence])}
                  />
                </TooltipWrapper>
              </Col>
            </FlexCol>
          </Row>
        </div>
      </React.StrictMode>
    );
  };
