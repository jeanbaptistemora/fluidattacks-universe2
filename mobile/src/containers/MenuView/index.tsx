/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */

import { NetworkStatus } from "apollo-boost";
import React from "react";
import { Query } from "react-apollo";
import { RefreshControl, ScrollView, ToastAndroid, View } from "react-native";
import { Appbar, Card, Paragraph, Title } from "react-native-paper";

import { Preloader } from "../../components/Preloader";
import { translate } from "../../utils/translations/translate";

import { PROJECTS_QUERY } from "./queries";
import { styles } from "./styles";
import { IMenuProps, IProject, PROJECTS_RESULT } from "./types";

const menuView: React.FunctionComponent<IMenuProps> = (): JSX.Element => {
  const { t } = translate;

  return (
    <View style={styles.container}>
      <Appbar.Header>
        <Appbar.Content title={t("menu.myProjects")} />
      </Appbar.Header>
      <Query query={PROJECTS_QUERY} notifyOnNetworkStatusChange={true}>
        {({ data, loading, error, refetch, networkStatus }: PROJECTS_RESULT): React.ReactNode => {
          const isRefetching: boolean = networkStatus === NetworkStatus.refetch;
          if (loading && !isRefetching) { return (<Preloader />); }
          if (error !== undefined) { ToastAndroid.show("Oops! There is an error.", ToastAndroid.SHORT); }

          return data === undefined
            ? <React.Fragment />
            : (
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
            );
        }}
      </Query>
    </View>
  );
};

export { menuView as MenuView };
