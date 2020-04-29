/* tslint:disable:jsx-no-multiline-js
 *
 * Necessary for mapping projects
 */

import { useQuery } from "@apollo/react-hooks";
import { ApolloError, NetworkStatus } from "apollo-client";
import _ from "lodash";
import React from "react";
import { Alert, RefreshControl, ScrollView, View } from "react-native";

import { Preloader } from "../../components/Preloader";
import { rollbar } from "../../utils/rollbar";

import { PROJECTS_QUERY } from "./queries";
import { styles } from "./styles";
import { IProject, IProjectsResult } from "./types";

const menuView: React.FunctionComponent = (): JSX.Element => {
  const { t } = translate;

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

  return (
    <View style={styles.container}>
      <Appbar.Header>
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
    </View>
  );
};

export { menuView as MenuView };
