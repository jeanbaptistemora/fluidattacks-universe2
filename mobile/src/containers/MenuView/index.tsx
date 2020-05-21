import { useQuery } from "@apollo/react-hooks";
import { ApolloError, NetworkStatus } from "apollo-client";
import { GoogleUser } from "expo-google-app-auth";
import * as SecureStore from "expo-secure-store";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { Alert, RefreshControl, ScrollView, View } from "react-native";
import { Card, Paragraph, Title, useTheme } from "react-native-paper";
import { useHistory } from "react-router-native";

import { Preloader } from "../../components/Preloader";
import { rollbar } from "../../utils/rollbar";

import { Header } from "./Header";
import { PROJECTS_QUERY } from "./queries";
import { styles } from "./styles";
import { IProject, IProjectsResult } from "./types";

const menuView: React.FunctionComponent = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { userInfo } = history.location.state as { userInfo: GoogleUser };
  const { colors } = useTheme();
  const { t } = useTranslation();

  // GraphQL operations
  const { data, loading, networkStatus, refetch } = useQuery<IProjectsResult>(PROJECTS_QUERY, {
    notifyOnNetworkStatusChange: true,
    onError: (error: ApolloError): void => {
      rollbar.error("An error occurred loading projects", error);
      Alert.alert(t("common.error.title"), t("common.error.msg"));
    },
  });

  const isRefetching: boolean = networkStatus === NetworkStatus.refetch;

  const projects: IProject[] = _.isUndefined(data) || _.isEmpty(data)
    ? []
    : data.me.projects;

  // Event handlers
  const handleLogout: (() => void) = async (): Promise<void> => {
    await SecureStore.deleteItemAsync("integrates_session");
    history.replace("/");
  };

  return (
    <React.StrictMode>
      <Header photoUrl={userInfo.photoUrl} userName={userInfo.name} onLogout={handleLogout} />
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <ScrollView
          contentContainerStyle={styles.projectList}
          refreshControl={<RefreshControl refreshing={isRefetching} onRefresh={refetch} />}
        >
          {projects.map((project: IProject, index: number): JSX.Element => (
            <Card key={index} style={styles.projectCard}>
              <Card.Content>
                <Title>{project.name.toUpperCase()}</Title>
                <Paragraph>{project.description}</Paragraph>
              </Card.Content>
            </Card>
          ))}
          <Preloader visible={loading && !isRefetching} />
        </ScrollView>
      </View>
    </React.StrictMode>
  );
};

export { menuView as MenuView };
