import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GoogleUser } from "expo-google-app-auth";
import * as SecureStore from "expo-secure-store";
/* tslint:disable: no-import-side-effect no-submodule-imports
 * Necessary polyfill due to a bug in RN for android
 * @see https://github.com/facebook/react-native/issues/19410
 */
import "intl";
import "intl/locale-data/jsonp/en-US";
import "intl/locale-data/jsonp/es-CO";
// tslint:enable
import _ from "lodash";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import { Alert, View } from "react-native";
import { Headline, Text, Title, useTheme } from "react-native-paper";
import { SvgCss } from "react-native-svg";
import { useHistory } from "react-router-native";

// tslint:disable-next-line: no-default-import
import { default as Border } from "../../../assets/percentBorder.svg";
import { Logo } from "../../components/Logo";
import { Preloader } from "../../components/Preloader";
import { rollbar } from "../../utils/rollbar";

import { Header } from "./Header";
import { PROJECTS_QUERY } from "./queries";
import { styles } from "./styles";
import { IProject, IProjectsResult } from "./types";

const dashboardView: React.FunctionComponent = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { userInfo } = history.location.state as { userInfo: GoogleUser };
  const { colors } = useTheme();
  const { t } = useTranslation();

  // GraphQL operations
  const { data, loading } = useQuery<IProjectsResult>(PROJECTS_QUERY, {
    onError: (error: ApolloError): void => {
      rollbar.error("An error occurred loading projects", error);
      Alert.alert(t("common.error.title"), t("common.error.msg"));
    },
  });

  const projects: IProject[] = _.isUndefined(data) || _.isEmpty(data)
    ? []
    : data.me.projects;

  const closedVulns: number = projects.reduce(
    (previousValue: number, project: IProject): number =>
      previousValue
      + project.closedVulnerabilities,
    0);

  const totalVulns: number = projects.reduce(
    (previousValue: number, project: IProject): number =>
      previousValue
      + project.openVulnerabilities
      + project.closedVulnerabilities,
    0);

  const remediatedPercentage: number = (closedVulns / totalVulns * 100);

  // Event handlers
  const handleLogout: (() => void) = async (): Promise<void> => {
    await SecureStore.deleteItemAsync("integrates_session");
    history.replace("/");
  };

  return (
    <React.StrictMode>
      <Header photoUrl={userInfo.photoUrl} userName={userInfo.name} onLogout={handleLogout} />
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.percentageContainer}>
          <SvgCss xml={Border} width={220} height={220} />
          <Text style={styles.percentageText}>
            {isNaN(remediatedPercentage) ? 0 : remediatedPercentage.toFixed(1)}%
          </Text>
        </View>
        <View style={styles.remediationContainer}>
          <Headline style={styles.remediatedText}>{t("dashboard.remediated")}</Headline>
          <Text>
            <Trans i18nKey="dashboard.vulnsFound" count={projects.length}>
              <Title>{{ totalVulns: totalVulns.toLocaleString() }}</Title>
            </Trans>
          </Text>
        </View>
        <Preloader visible={loading} />
        <View style={styles.bottom}>
          <Logo width={180} height={40} fill={colors.text} />
        </View>
      </View>
    </React.StrictMode>
  );
};

export { dashboardView as DashboardView };
