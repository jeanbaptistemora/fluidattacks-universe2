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
import {
  Alert,
  Animated,
  AppState,
  AppStateStatus,
  Dimensions,
  ScrollViewProps,
  View,
} from "react-native";
import { Headline, useTheme } from "react-native-paper";
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
  const { width } = Dimensions.get("window");

  // State management
  const scrollPosition: Animated.Value = React.useRef(
    new Animated.Value(0)).current;
  const currentPage: Animated.AnimatedDivision = Animated.divide(
    scrollPosition, width);

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
      totalGroups: 0,
    },
    name: "",
  };
  const orgs: IOrganization[] = _.isUndefined(data) || _.isEmpty(data)
    ? [emptyOrg]
    : data.me.organizations.length === 0
      ? [emptyOrg]
      : _.sortBy(data.me.organizations.filter(hasAnalytics), "name");

  // Event handlers
  const handleLogout: (() => void) = async (): Promise<void> => {
    await logout();
    client.stop();
    await client.clearStore();
    history.replace("/Login");
  };

  const handleScroll: ScrollViewProps["onScroll"] = Animated.event(
    [{ nativeEvent: { contentOffset: { x: scrollPosition } } }],
    { useNativeDriver: true },
  );

  return (
    <React.StrictMode>
      <Header user={user} onLogout={handleLogout} />
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <Animated.ScrollView
          decelerationRate="fast"
          horizontal={true}
          onScroll={handleScroll}
          pagingEnabled={true}
          scrollEventThrottle={16}
          showsHorizontalScrollIndicator={false}
          snapToAlignment="center"
          style={styles.scrollContainer}
        >
          {orgs.map((org: IOrganization): JSX.Element => (
            <Indicators key={org.name} org={org} />
          ))}
        </Animated.ScrollView>
        <View style={styles.dotsContainer}>
          {orgs.map((_0: IOrganization, index: number): JSX.Element => {
            const opacityScale: number = 0.3;
            const opacity: Animated.AnimatedInterpolation =
              currentPage.interpolate({
                inputRange: [index - 1, index, index + 1],
                outputRange: [opacityScale, 1, opacityScale],
              });

            return (
              <Animated.View key={index} style={{ opacity }}>
                <Headline>&bull;</Headline>
              </Animated.View>
            );
          })}
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
