import { MaterialIcons } from "@expo/vector-icons";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import { View } from "react-native";
import { Headline, Subheading, Text, Title, useTheme } from "react-native-paper";
import { SvgCss } from "react-native-svg";

// tslint:disable-next-line: no-default-import
import { default as Border } from "../../../../assets/percentBorder.svg";
import { IOrganization } from "../types";

import { styles } from "./styles";

/** Indicators data structure */
interface IIndicators {
  closed: number;
  percentage: number;
  total: number;
}

type CalcIndicatorsFn = ((
  org: IOrganization,
  kind: keyof IOrganization["analytics"],
) => IIndicators);

const calcIndicators: CalcIndicatorsFn = (
  org: IOrganization,
  kind: keyof IOrganization["analytics"],
): IIndicators => {
  const closedVulns: number = org.analytics[kind].closed;

  const totalVulns: number =
    org.analytics[kind].open
    + org.analytics[kind].closed;

  const remediationPercentage: number = (closedVulns / totalVulns * 100);

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

const indicators: React.FC<IIndicatorsProps> = (
  props: IIndicatorsProps,
): JSX.Element => {
  const { org } = props;
  const { colors } = useTheme();
  const { t } = useTranslation();

  const current: IIndicators = calcIndicators(org, "current");
  const previous: IIndicators = calcIndicators(org, "previous");
  const percentageDiff: number =
    parseFloat((current.percentage - previous.percentage).toFixed(1));

  const color: string = percentageDiff === 0
    ? colors.text
    : percentageDiff > 0
      ? "#0F9D58"
      : "#DB4437";

  return (
    <View style={styles.container}>
      <View style={styles.percentageContainer}>
        <SvgCss xml={Border} width={220} height={220} />
        <Text style={styles.percentageText}>
          {parseFloat(current.percentage.toFixed(1))}%
        </Text>
      </View>
      <View style={styles.remediationContainer}>
        <View style={styles.diff}>
          {percentageDiff === 0
            ? <MaterialIcons name="remove" size={24} color={color} />
            : percentageDiff > 0
              ? <MaterialIcons name="arrow-upward" size={24} color={color} />
              : <MaterialIcons
                name="arrow-downward"
                size={24}
                color={color}
              />
          }
          <Title style={{ color }}>
            {percentageDiff > 0 ? "+" : undefined}{percentageDiff}%
          </Title>
        </View>
        <Text>{t("dashboard.diff")}</Text>
        <Headline style={styles.remediatedText}>
          {t("dashboard.remediated")}
        </Headline>
        <Subheading>
          <Trans i18nKey="dashboard.vulnsFound" count={org.totalGroups}>
            <Title>{{ totalVulns: current.total.toLocaleString() }}</Title>
          </Trans>
        </Subheading>
      </View>
    </View>
  );
};

export { indicators as Indicators };
