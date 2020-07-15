import { useQuery } from "@apollo/react-hooks";
import { wait } from "@apollo/react-testing";
import { ApolloError, NetworkStatus } from "apollo-client";
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
import { About } from "../../components/About";
import { Logo } from "../../components/Logo";
import { Preloader } from "../../components/Preloader";
import { rollbar } from "../../utils/rollbar";
import { IAuthState, logout } from "../../utils/socialAuth";

import { Header } from "./Header";
import { ORGS_QUERY } from "./queries";
import { styles } from "./styles";
import { IOrganization, IOrgsResult } from "./types";

const dashboardView: React.FunctionComponent = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { user } = history.location.state as IAuthState;
  const { colors } = useTheme();
  const { t } = useTranslation();

  // GraphQL operations
  const { client, data, networkStatus, refetch } = useQuery<IOrgsResult>(
    ORGS_QUERY, {
    errorPolicy: "all",
    notifyOnNetworkStatusChange: true,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - Document not found":
            // Ignore orgs without analytics
            break;
          default:
            rollbar.error("An error occurred loading dashboard data", error);
            Alert.alert(t("common.error.title"), t("common.error.msg"));
        }
      });
    },
  });

  // Side effects
  let lockTimerId: number | undefined;
  let locked: boolean = false;

  const handleAppStateChange: (state: AppStateStatus) => void = async (
    state: AppStateStatus,
  ): Promise<void> => {
    if (state === "active") {
      await wait(1);
      /**
       * This apparently redundant flag is necessary as a workaround since
       * Android allows the timer to run in background but the callback will be
       * executed as soon as the app is foregrounded again
       *
       * @see https://git.io/JJYeb
       */
      if (lockTimerId !== undefined && !locked) {
        clearTimeout(lockTimerId);
        locked = false;
        await refetch();
      }
    } else if (state === "background") {
      const minutesToLock: number = 5;
      const minutesInSec: number = 60;
      const secondsInMs: number = 1000;

      lockTimerId = setTimeout(
        (): void => { locked = true; history.replace("/"); },
        minutesToLock * minutesInSec * secondsInMs,
      );
    }
  };

  const onMount: (() => void) = (): (() => void) => {
    AppState.addEventListener("change", handleAppStateChange);

    return (): void => {
      AppState.removeEventListener("change", handleAppStateChange);
    };
  };
  React.useEffect(onMount, []);

  const hasAnalytics: ((organization: IOrganization) => boolean) = (
    organization: IOrganization,
  ): boolean => !_.isNil(organization.analytics);

  const orgs: IOrganization[] = _.isNil(data) || _.isEmpty(data)
    ? []
    : data.me.organizations.filter(hasAnalytics);

  const closedVulns: number = orgs.reduce(
    (previousValue: number, organization: IOrganization): number =>
      previousValue
      + organization.analytics.current.closed,
    0);

  const totalVulns: number = orgs.reduce(
    (previousValue: number, organization: IOrganization): number =>
      previousValue
      + organization.analytics.current.open
      + organization.analytics.current.closed,
    0);

  const totalGroups: number = orgs.reduce(
    (previousValue: number, organization: IOrganization): number =>
      previousValue
      + organization.totalGroups,
    0);

  const remediatedPercentage: number = (closedVulns / totalVulns * 100);

  // Event handlers
  const handleLogout: (() => void) = async (): Promise<void> => {
    await logout();
    client.stop();
    await client.clearStore();
    history.replace("/Login");
  };

  return (
    <React.StrictMode>
      <Header
        photoUrl={user.photoUrl}
        userName={user.fullName}
        onLogout={handleLogout}
      />
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.percentageContainer}>
          <SvgCss xml={Border} width={220} height={220} />
          <Text style={styles.percentageText}>
            {isNaN(remediatedPercentage)
              ? 0
              : parseFloat(remediatedPercentage.toFixed(1))}%
          </Text>
        </View>
        <View style={styles.remediationContainer}>
          <Headline style={styles.remediatedText}>
            {t("dashboard.remediated")}
          </Headline>
          <Text>
            <Trans i18nKey="dashboard.vulnsFound" count={totalGroups}>
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
          <About />
        </View>
      </View>
    </React.StrictMode>
  );
};

export { dashboardView as DashboardView };
