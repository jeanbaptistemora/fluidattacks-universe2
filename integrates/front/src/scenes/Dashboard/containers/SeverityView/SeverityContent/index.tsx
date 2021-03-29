import type { ISeverityAttr } from "../types";
import React from "react";
import { SeverityTile } from "./tile";
import type { StyledComponent } from "styled-components";
import { TooltipWrapper } from "components/TooltipWrapper";
import styled from "styled-components";
import { useTranslation } from "react-i18next";
import {
  attackComplexityBgColor,
  attackComplexityOptions,
  attackVectorBgColor,
  attackVectorOptions,
  availabilityImpactBgColor,
  availabilityImpactOptions,
} from "../utils";

const Row: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "w-100-m w-25-ns pa2",
})``;

const Col: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "pa2 w-100 mb3-l mb2-m mb1-ns",
})``;

const FlexCol: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "flex flex-column items-center",
})``;

export const SeverityContent: React.FC<
  ISeverityAttr["finding"]["severity"]
> = ({
  attackVector,
  attackComplexity,
  availabilityImpact,
}: ISeverityAttr["finding"]["severity"]): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <div className={"flex flex-wrap items-center h-100 w-100"}>
        <Row>
          <FlexCol>
            <Col />
            <Col />
          </FlexCol>
        </Row>
        <Row>
          <FlexCol>
            <Col>
              <TooltipWrapper
                id={"attackVectorTooltip"}
                message={t(
                  attackVectorOptions[attackVector].replace(/text/u, "tooltip")
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
                    /text/u,
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
            <Col />
            <Col />
          </FlexCol>
        </Row>
        <Row>
          <FlexCol>
            <Col>
              <TooltipWrapper
                id={"availabilityImpactTooltip"}
                message={t(
                  availabilityImpactOptions[availabilityImpact].replace(
                    /text/u,
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
            <Col />
            <Col />
          </FlexCol>
        </Row>
        <Row>
          <FlexCol>
            <Col />
            <Col />
          </FlexCol>
        </Row>
      </div>
    </React.StrictMode>
  );
};
