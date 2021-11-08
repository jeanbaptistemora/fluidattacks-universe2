// Needed to override styles
/* eslint-disable react/forbid-component-props */
import { MaterialIcons } from "@expo/vector-icons";
import _ from "lodash";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import { View } from "react-native";
import {
  Headline,
  Subheading,
  Text,
  Title,
  useTheme,
} from "react-native-paper";
import { SvgCss } from "react-native-svg";

import { styles } from "./styles";

import Border from "../../../../assets/percentBorder.svg";
import type { IOrganization } from "../types";

/** Indicators data structure */
interface IIndicators {
  closed: number;
  percentage: number;
  total: number;
}

// eslint-disable-next-line @typescript-eslint/no-type-alias
type CalcIndicatorsFn = (
  org: IOrganization,
  kind: "current" | "previous"
) => IIndicators;

const calcIndicators: CalcIndicatorsFn = (
  org: IOrganization,
  kind: "current" | "previous"
): IIndicators => {
  const closedVulns: number = org.analytics[kind].closed;

  const totalVulns: number =
    org.analytics[kind].open + org.analytics[kind].closed;

  const percentage = 100;
  const remediationPercentage: number = (closedVulns / totalVulns) * percentage;

  return {
    closed: closedVulns,
    percentage: isNaN(remediationPercentage) ? 0 : remediationPercentage,
    total: totalVulns,
  };
};

/** Indicators props structure */
interface IIndicatorsProps {
  org: IOrganization;
}

const Indicators: React.FC<IIndicatorsProps> = (
  props: IIndicatorsProps
): JSX.Element => {
  const { org } = props;
  const { colors } = useTheme();
  const { t } = useTranslation();

  const { totalGroups } = org.analytics;
  const current: IIndicators = calcIndicators(org, "current");
  const previous: IIndicators = calcIndicators(org, "previous");
  const percentageDiff: number = parseFloat(
    (current.percentage - previous.percentage).toFixed(1)
  );

  const color: string =
    percentageDiff === 0
      ? colors.text
      : percentageDiff > 0
      ? "#0F9D58"
      : "#DB4437";

  return (
    <View style={styles.container}>
      <Title>{_.capitalize(org.name)}</Title>
      <View style={styles.percentageContainer}>
        <SvgCss height={220} width={220} xml={Border} />
        <Text style={styles.percentageText}>
          {parseFloat(current.percentage.toFixed(1))}
          {"%"}
        </Text>
      </View>
      <View style={styles.remediationContainer}>
        <View style={styles.diff}>
          {percentageDiff === 0 ? (
            <MaterialIcons color={color} name={"remove"} size={24} />
          ) : percentageDiff > 0 ? (
            <MaterialIcons color={color} name={"arrow-upward"} size={24} />
          ) : (
            <MaterialIcons color={color} name={"arrow-downward"} size={24} />
          )}
          <Title style={{ color }}>
            {percentageDiff > 0 ? "+" : undefined}
            {percentageDiff}
            {"%"}
          </Title>
        </View>
        <Text>{t("dashboard.diff")}</Text>
        <Headline style={styles.remediatedText}>
          {t("dashboard.remediated")}
        </Headline>
        <Subheading>
          <Trans count={totalGroups} i18nKey={"dashboard.vulnsFound"}>
            <Title>
              {{
                totalVulns: Number(current.total.toFixed(1)).toLocaleString(),
              }}
            </Title>
          </Trans>
        </Subheading>
      </View>
    </View>
  );
};

export { Indicators, IIndicatorsProps };
