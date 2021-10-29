// Allow some necesary mutations/side effects
/* eslint-disable fp/no-let */
/* eslint-disable @typescript-eslint/init-declarations */
/* eslint-disable fp/no-mutation */
// Needed to override styles
/* eslint-disable react/forbid-component-props */
import { NetworkStatus, useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  addNotificationReceivedListener,
  addNotificationResponseReceivedListener,
} from "expo-notifications";
import type { Notification, NotificationResponse } from "expo-notifications";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";
import {
  Alert,
  Animated,
  AppState,
  Dimensions,
  Platform,
  View,
} from "react-native";
import type { AppStateStatus, ScrollViewProps } from "react-native";
import { Headline, Text, useTheme } from "react-native-paper";
import { useHistory } from "react-router-native";
import wait from "waait";

import { Header } from "./Header";
import { getOrgs } from "./helpers";
import { Indicators } from "./Indicators";
import { ADD_PUSH_TOKEN_MUTATION, ORGS_QUERY } from "./queries";
import { styles } from "./styles";
import type { IOrganization, IOrgsResult } from "./types";

import { About } from "../../components/About";
import { Preloader } from "../../components/Preloader";
import { LOGGER } from "../../utils/logger";
import { getPushToken } from "../../utils/notifications";
import { useSessionToken } from "../../utils/sessionToken/context";
import { logout } from "../../utils/socialAuth";
import type { IAuthState } from "../../utils/socialAuth";

import "intl";
import "intl/locale-data/jsonp/en-US";
import "intl/locale-data/jsonp/es-CO";

const emptyOrg: IOrganization = {
  analytics: {
    current: { closed: 0, open: 0 },
    previous: { closed: 0, open: 0 },
    totalGroups: 0,
  },
  name: "",
};

const DashboardView: React.FunctionComponent = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { user } = history.location.state as IAuthState;
  const { colors } = useTheme();
  const { t } = useTranslation();
  const { width } = Dimensions.get("window");
  const [, setSessionToken] = useSessionToken();

  // State management
  const scrollPosition: Animated.Value = useRef(new Animated.Value(0)).current;
  const currentPage: Animated.AnimatedDivision = Animated.divide(
    scrollPosition,
    width
  );

  // GraphQL operations
  const { client, data, networkStatus, refetch } = useQuery<IOrgsResult>(
    ORGS_QUERY,
    {
      errorPolicy: "all",
      notifyOnNetworkStatusChange: true,
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - Document not found":
              // Ignore orgs without analytics
              break;
            default:
              LOGGER.warning("An error occurred loading dashboard data", error);
              Alert.alert(t("common.error.title"), t("common.error.msg"));
          }
        });
      },
    }
  );

  const [addPushToken] = useMutation(ADD_PUSH_TOKEN_MUTATION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        LOGGER.error("Couldn't add push token", error);
      });
    },
  });

  // Side effects
  let lockTimerId: unknown | undefined;
  let locked: boolean = false;

  const handleAppStateChange: (state: AppStateStatus) => void = async (
    state: AppStateStatus
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
        clearTimeout(lockTimerId as number);
        locked = false;
        await refetch();
      }
    } else if (state === "background") {
      const minutesToLock: number = 5;
      const minutesInSec: number = 60;
      const secondsInMs: number = 1000;

      lockTimerId = setTimeout((): void => {
        locked = true;
        history.replace("/");
      }, minutesToLock * minutesInSec * secondsInMs);
    }
  };

  const registerPushToken: () => void = async (): Promise<void> => {
    const token: string = await getPushToken();

    if (!_.isEmpty(token)) {
      await addPushToken({ variables: { token } });
    }
  };

  const handleIncomingNotifs: (event: Notification) => void = (
    notification: Notification
  ): void => {
    const { body, title } = notification.request.content;

    if (body !== null && title !== null) {
      // Alerts won't open immediatly after opening the app (RN 0.63 bug)
      const delay: number = Platform.select({ android: 100, default: 0 });
      setTimeout((): void => {
        Alert.alert(title, body);
      }, delay);
    }
  };

  const onMount: () => void = (): (() => void) => {
    AppState.addEventListener("change", handleAppStateChange);
    type Subscription = ReturnType<typeof addNotificationReceivedListener>;
    const notificationListeners: Subscription[] = [
      addNotificationResponseReceivedListener(
        ({ notification }: NotificationResponse): void => {
          handleIncomingNotifs(notification);
        }
      ),
      addNotificationReceivedListener(handleIncomingNotifs),
    ];
    registerPushToken();

    return (): void => {
      AppState.removeEventListener("change", handleAppStateChange);
      notificationListeners.forEach((listener: Subscription): void => {
        listener.remove();
      });
    };
  };
  // We only want this to run when the component mounts.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(onMount, []);

  const orgs: IOrganization[] = getOrgs(data, emptyOrg);

  // Event handlers
  const handleLogout: () => void = async (): Promise<void> => {
    await logout(setSessionToken);
    client.stop();
    await client.clearStore();
    history.replace("/Login");
  };

  const handleScroll: ScrollViewProps["onScroll"] = Animated.event(
    [{ nativeEvent: { contentOffset: { x: scrollPosition } } }],
    { useNativeDriver: true }
  );

  return (
    <React.StrictMode>
      {/* Unexpected behavior with no-bind */}
      {/* eslint-disable-next-line react/jsx-no-bind */}
      <Header onLogout={handleLogout} user={user} />
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <Animated.ScrollView
          decelerationRate={"fast"}
          horizontal={true}
          onScroll={handleScroll}
          pagingEnabled={true}
          scrollEventThrottle={16}
          showsHorizontalScrollIndicator={false}
          snapToAlignment={"center"}
          style={styles.scrollContainer}
        >
          {orgs.map(
            (org: IOrganization): JSX.Element => (
              <Indicators key={org.name} org={org} />
            )
          )}
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
              <Animated.View key={index.toString()} style={{ opacity }}>
                {/* Needed to properly render the html bullet over the logo*/}
                {/* eslint-disable-next-line react/jsx-no-literals*/}
                <Headline>&bull;</Headline>
              </Animated.View>
            );
          })}
        </View>
        <Preloader
          visible={[NetworkStatus.loading, NetworkStatus.refetch].includes(
            networkStatus
          )}
        />
        <View style={styles.bottom}>
          <Text>{t("common.slogan")}</Text>
          <About />
        </View>
      </View>
    </React.StrictMode>
  );
};

export { DashboardView };
