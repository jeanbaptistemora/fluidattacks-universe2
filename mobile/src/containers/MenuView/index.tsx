/* tslint:disable:jsx-no-multiline-js
 *
 * Necessary for mapping projects
 */

import { useQuery } from "@apollo/react-hooks";
import { NetworkStatus } from "apollo-client";
import _ from "lodash";
import React from "react";
import { RefreshControl, ScrollView, View } from "react-native";
import { Appbar, Card, Paragraph, Title } from "react-native-paper";

import { Preloader } from "../../components/Preloader";
import * as errorDialog from "../../utils/errorDialog";
import { translate } from "../../utils/translations/translate";

import { PROJECTS_QUERY } from "./queries";
import { styles } from "./styles";
import { IMenuProps, IProject, IProjectsResult } from "./types";

const menuView: React.FunctionComponent<IMenuProps> = (): JSX.Element => {
  const { t } = translate;

  // GraphQL operations
  const { data, loading, networkStatus, refetch } = useQuery<IProjectsResult>(PROJECTS_QUERY, {
    notifyOnNetworkStatusChange: true,
    onError: (): void => {
      errorDialog.show();
    },
  });

  const isRefetching: boolean = networkStatus === NetworkStatus.refetch;
  if (loading && !isRefetching) {
    return (<Preloader />);
  }

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  return (
    <View style={styles.container}>
      <Appbar.Header>
        <Appbar.Content title={t("menu.myProjects")} />
      </Appbar.Header>
              <ScrollView
                contentContainerStyle={styles.projectList}
                refreshControl={<RefreshControl refreshing={isRefetching} onRefresh={refetch} />}
              >
                {data.me.projects.map((project: IProject, index: number): JSX.Element => (
                  <Card key={index} style={styles.projectCard}>
                    <Card.Content>
                      <Title>{project.name.toUpperCase()}</Title>
                      <Paragraph>{project.description}</Paragraph>
                    </Card.Content>
                  </Card>
                ))}
              </ScrollView>
    </View>
  );
};

export { menuView as MenuView };
