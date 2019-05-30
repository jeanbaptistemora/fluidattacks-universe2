/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */

import { SecureStore } from "expo";
import _ from "lodash";
import React from "react";
import { Mutation, MutationFn, MutationResult } from "react-apollo";
import { Image, Text, View } from "react-native";

import { MutationTrigger } from "../../components/MutationTrigger";
import { Preloader } from "../../components/Preloader";
import * as errorDialog from "../../utils/errorDialog";
import { translate } from "../../utils/translations/translate";

import { SIGN_IN_MUTATION } from "./queries";
import { styles } from "./styles";
import { IWelcomeProps, SIGN_IN_RESULT } from "./types";

const welcomeView: React.FunctionComponent<IWelcomeProps> = (props: IWelcomeProps): JSX.Element => {
  const { authProvider, authToken, userInfo } = props.location.state;
  const { t } = translate;

  const handleMutationResult: ((data: SIGN_IN_RESULT) => void) = (data: SIGN_IN_RESULT): void => {
    if (data !== undefined) {
      if (data.signIn.success) {
        SecureStore.setItemAsync("integrates_session", data.signIn.sessionJwt)
          .then((): void => {
            if (data.signIn.authorized) {
              props.history.push("/Menu");
            }
          })
          .catch();
      } else {
        errorDialog.show();
      }
    }
  };

  return (
    <View style={styles.container}>
      <Image style={styles.profilePicture} source={{ uri: userInfo.photoUrl }} />
      <Text style={styles.greeting}>{t("welcome.greetingText")} {userInfo.givenName}!</Text>
      <Mutation
        mutation={SIGN_IN_MUTATION}
        variables={{ authToken, provider: authProvider }}
        onCompleted={handleMutationResult}
      >
        {(doAuth: MutationFn, { data, error, loading, called }: MutationResult<SIGN_IN_RESULT>): React.ReactNode => {
          if (loading) { return (<Preloader />); }
          if (error !== undefined) { errorDialog.show(); }
          if (!called) { return (<MutationTrigger onMount={doAuth} />); }
          const isAuthorized: boolean = data !== undefined && data.signIn.authorized;

          return isAuthorized
            ? <Preloader />
            : <Text style={styles.unauthorized}>{t("welcome.unauthorized")}</Text>;
        }}
      </Mutation>
    </View>
  );
};

export { welcomeView as WelcomeView };
