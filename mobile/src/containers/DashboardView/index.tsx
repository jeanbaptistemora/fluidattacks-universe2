import { useQuery } from "@apollo/react-hooks";
import { ApolloError, NetworkStatus } from "apollo-client";
import * as Updates from "expo-updates";
import { GraphQLError } from "graphql";
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
import { Alert, AppState, AppStateStatus, View } from "react-native";
import { Headline, Text, Title, useTheme } from "react-native-paper";
import { SvgCss } from "react-native-svg";
import { useHistory } from "react-router-native";

// tslint:disable-next-line: no-default-import
import { default as Border } from "../../../assets/percentBorder.svg";
import { Logo } from "../../components/Logo";
import { Preloader } from "../../components/Preloader";
import { rollbar } from "../../utils/rollbar";
import { IAuthState, logout } from "../../utils/socialAuth";

import { Header } from "./Header";
import { GROUPS_QUERY } from "./queries";
import { styles } from "./styles";
import { IGroup, IGroupsResult } from "./types";

const dashboardView: React.FunctionComponent = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { user } = history.location.state as IAuthState;
  const { colors } = useTheme();
  const { t } = useTranslation();

  // GraphQL operations
  const { client, data, networkStatus, refetch } = useQuery<IGroupsResult>(GROUPS_QUERY, {
    errorPolicy: "all",
    notifyOnNetworkStatusChange: true,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Access denied":
            // Ignore groups without integrates service
            break;
          default:
            rollbar.error("An error occurred loading groups", error);
            Alert.alert(t("common.error.title"), t("common.error.msg"));
        }
      });
    },
  });

  // Side effects
  const handleAppStateChange: (state: AppStateStatus) => void = async (
    state: AppStateStatus,
  ): Promise<void> => {
    if (state === "active") {
      await refetch();
    }
  };

  const onMount: (() => void) = (): (() => void) => {
    AppState.addEventListener("change", handleAppStateChange);

    return (): void => {
      AppState.removeEventListener("change", handleAppStateChange);
    };
  };
  React.useEffect(onMount, []);

  const hasIntegrates: ((group: IGroup) => boolean) = (group: IGroup): boolean =>
    !_.isNil(group.serviceAttributes)
    && group.serviceAttributes.includes("has_integrates");

  const groups: IGroup[] = _.isUndefined(data) || _.isEmpty(data)
    ? []
    : data.me.groups.filter(hasIntegrates);

  const closedVulns: number = groups.reduce(
    (previousValue: number, group: IGroup): number =>
      previousValue
      + group.closedVulnerabilities,
    0);

  const totalVulns: number = groups.reduce(
    (previousValue: number, group: IGroup): number =>
      previousValue
      + group.openVulnerabilities
      + group.closedVulnerabilities,
    0);

  const remediatedPercentage: number = (closedVulns / totalVulns * 100);

  // Event handlers
  const handleLogout: (() => void) = async (): Promise<void> => {
    await logout();
    await client.clearStore();
    history.replace("/");
  };

  return (
    <React.StrictMode>
      <Header photoUrl={user.photoUrl} userName={user.fullName} onLogout={handleLogout} />
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.percentageContainer}>
          <SvgCss xml={Border} width={220} height={220} />
          <Text style={styles.percentageText}>
            {isNaN(remediatedPercentage) ? 0 : parseFloat(remediatedPercentage.toFixed(1))}%
          </Text>
        </View>
        <View style={styles.remediationContainer}>
          <Headline style={styles.remediatedText}>{t("dashboard.remediated")}</Headline>
          <Text>
            <Trans i18nKey="dashboard.vulnsFound" count={groups.length}>
              <Title>{{ totalVulns: totalVulns.toLocaleString() }}</Title>
            </Trans>
          </Text>
        </View>
        <Preloader
          visible={[
            NetworkStatus.loading,
            NetworkStatus.refetch,
          ].includes(networkStatus)}
        />
        <View style={styles.bottom}>
          <Logo width={180} height={40} fill={colors.text} />
          <Text style={styles.text}>v. {(Updates.manifest as Updates.Manifest).version}</Text>
        </View>
      </View>
    </React.StrictMode>
  );
};

export { dashboardView as DashboardView };
