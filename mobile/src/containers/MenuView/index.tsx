import { useQuery } from "@apollo/react-hooks";
import { ApolloError, NetworkStatus } from "apollo-client";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { Alert, Platform, RefreshControl, ScrollView, View } from "react-native";
/* tslint:disable-next-line: no-import-side-effect
 * Necessary for importing unindexed module definitions
 */
import "react-native-gesture-handler";
/* tslint:disable-next-line: no-submodule-imports
 * Necessary for importing unindexed types
 */
import DrawerLayout from "react-native-gesture-handler/DrawerLayout";
import { Appbar, Card, Paragraph, Title, useTheme } from "react-native-paper";

import { Preloader } from "../../components/Preloader";
import { rollbar } from "../../utils/rollbar";

import { PROJECTS_QUERY } from "./queries";
import { Sidebar } from "./Sidebar";
import { styles } from "./styles";
import { IProject, IProjectsResult } from "./types";

const menuView: React.FunctionComponent = (): JSX.Element => {
  const { colors } = useTheme();
  const { t } = useTranslation();
  /* tslint:disable-next-line: no-null-keyword
   * React refs cannot be initialized as 'undefined'
   */
  const drawer: React.RefObject<DrawerLayout> = React.useRef(null);

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

  const openDrawer: (() => void) = (): void => {
    drawer.current?.openDrawer();
  };

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <DrawerLayout
        drawerBackgroundColor="#DDDDDD"
        drawerPosition="left"
        drawerType={Platform.select({ android: "front", ios: "slide" })}
        drawerWidth={200}
        ref={drawer}
        renderNavigationView={Sidebar}
      >
        <Appbar.Header>
          <Appbar.Action icon="menu" onPress={openDrawer} />
          <Appbar.Content title={t("menu.myProjects")} />
        </Appbar.Header>
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
      </DrawerLayout>
    </View>
  );
};

export { menuView as MenuView };
