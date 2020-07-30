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
import { useTranslation } from "react-i18next";
import { Alert, AppState, AppStateStatus, ScrollView, View } from "react-native";
import { useTheme } from "react-native-paper";
import { useHistory } from "react-router-native";

import { About } from "../../components/About";
import { Logo } from "../../components/Logo";
import { Preloader } from "../../components/Preloader";
import { rollbar } from "../../utils/rollbar";
import { IAuthState, logout } from "../../utils/socialAuth";

import { Header } from "./Header";
import { Indicators } from "./Indicators";
import { ORGS_QUERY } from "./queries";
import { styles } from "./styles";
import { IOrganization, IOrgsResult } from "./types";

const hasAnalytics: ((organization: IOrganization) => boolean) = (
  organization: IOrganization,
): boolean => !_.isNil(organization.analytics);

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
  const emptyOrg: IOrganization = {
    analytics: {
      current: { closed: 0, open: 0 },
      previous: { closed: 0, open: 0 },
    },
    name: "",
    totalGroups: 0,
  };
  const orgs: IOrganization[] = _.isUndefined(data) || _.isEmpty(data)
    ? [emptyOrg]
    : data.me.organizations.length === 0
      ? [emptyOrg]
      : data.me.organizations.filter(hasAnalytics);

  // Event handlers
  const handleLogout: (() => void) = async (): Promise<void> => {
    await logout();
    client.stop();
    await client.clearStore();
    history.replace("/Login");
  };

  return (
    <React.StrictMode>
      <Header user={user} onLogout={handleLogout} />
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <ScrollView
          decelerationRate="fast"
          horizontal={true}
          pagingEnabled={true}
          showsHorizontalScrollIndicator={false}
          snapToAlignment="center"
        >
          {orgs.map((org: IOrganization): JSX.Element => (
            <Indicators key={org.name} org={org} />
          ))}
        </ScrollView>
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
