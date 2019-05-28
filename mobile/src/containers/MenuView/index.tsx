/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */

import React from "react";
import { Query } from "react-apollo";
import { Text, ToastAndroid, View } from "react-native";

import { Preloader } from "../../components/Preloader";
import { translate } from "../../utils/translations/translate";

import { PROJECTS_QUERY } from "./queries";
import { styles } from "./styles";
import { IMenuProps, IProject, PROJECTS_RESULT } from "./types";

const menuView: React.FunctionComponent<IMenuProps> = (): JSX.Element => {
  const { t } = translate;

  return (
    <View style={styles.container}>
      <Text>{t("menu.myProjects")}</Text>
      <Query query={PROJECTS_QUERY}>
        {({ data, loading, error }: PROJECTS_RESULT): React.ReactNode => {
          if (loading) { return (<Preloader />); }
          if (error !== undefined) { ToastAndroid.show("Oops! There is an error.", ToastAndroid.SHORT); }

          return data === undefined
            ? <React.Fragment />
            : (
              <View>
                {data.me.projects.map((project: IProject, index: number): JSX.Element => (
                  <Text key={index}>{project.name}</Text>
                ))}
              </View>
            );
        }}
      </Query>
    </View>
  );
};

export { menuView as MenuView };
