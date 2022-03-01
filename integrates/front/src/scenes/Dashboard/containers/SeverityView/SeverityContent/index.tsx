import React from "react";
import { useTranslation } from "react-i18next";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { SeverityTile } from "./tile";

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

    return (
      <React.StrictMode>
        <div className={"flex flex-wrap items-center h-100 w-100"}>
          <Row>
            <FlexCol>
              <Col>
                <TooltipWrapper
                  id={"userInteractionTooltip"}
                  message={t(
                    userInteractionOptions[userInteraction].replace(
                      /label/u,
                      "tooltip"
                    )
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
                  message={t(
                    castPrivileges(severityScope)[privilegesRequired].replace(
                      /label/u,
                      "tooltip"
                    )
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
                  message={t(
                    attackVectorOptions[attackVector].replace(
                      /label/u,
                      "tooltip"
                    )
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
                  message={t(
                    attackComplexityOptions[attackComplexity].replace(
                      /label/u,
                      "tooltip"
                    )
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
                  message={t(
                    exploitabilityOptions[exploitability].replace(
                      /label/u,
                      "tooltip"
                    )
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
                  message={t(
                    severityScopeOptions[severityScope].replace(
                      /label/u,
                      "tooltip"
                    )
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
                  message={t(
                    availabilityImpactOptions[availabilityImpact].replace(
                      /label/u,
                      "tooltip"
                    )
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
                  message={t(
                    integrityImpactOptions[integrityImpact].replace(
                      /label/u,
                      "tooltip"
                    )
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
                  message={t(
                    confidentialityImpactOptions[confidentialityImpact].replace(
                      /label/u,
                      "tooltip"
                    )
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
                  message={t(
                    remediationLevelOptions[remediationLevel].replace(
                      /label/u,
                      "tooltip"
                    )
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
                  message={t(
                    reportConfidenceOptions[reportConfidence].replace(
                      /label/u,
                      "tooltip"
                    )
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
