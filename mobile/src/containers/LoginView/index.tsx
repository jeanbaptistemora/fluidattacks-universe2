import React from "react";
import { Button, Image, View } from "react-native";
import { connect, ConnectedComponentClass, MapDispatchToProps, MapStateToProps } from "react-redux";
import { RedirectProps } from "react-router";
import { Redirect, RouteComponentProps } from "react-router-native";

// tslint:disable-next-line: no-default-import
import { default as FluidLogo } from "../../../assets/logo.png";
import { IState, ThunkDispatcher } from "../../store";
import { translate } from "../../utils/translations/translate";

import * as actions from "./actions";
import { ILoginState } from "./reducer";
import { styles } from "./styles";

type ILoginBaseProps = RouteComponentProps;

/**
 * Redux actions dispatched from LoginView
 */
interface ILoginDispatchProps {
  onGoogleLogin(): void;
}

export type ILoginProps = ILoginBaseProps & (ILoginState & ILoginDispatchProps);

export const loginView: React.FunctionComponent<ILoginProps> = (props: ILoginProps): JSX.Element => {
  const handleGoogleButtonClick: (() => void) = (): void => { props.onGoogleLogin(); };

  const { t } = translate;

  const redirectParams: RedirectProps["to"] = {
    pathname: "/Welcome",
    state: {
      authProvider: props.authProvider,
      authToken: props.authToken,
      userInfo: props.userInfo,
    },
  };

  return props.isAuthenticated ? <Redirect to={redirectParams} /> : (
    <View style={styles.container}>
      <Image source={FluidLogo} style={styles.logo} />
      <View style={styles.buttonsContainer}>
        <Button
          disabled={props.isLoading}
          color="#cc0000"
          onPress={handleGoogleButtonClick}
          title={props.isLoading ? t("login.authLoadingText") : t("login.btnGoogleText")}
        />
      </View>
    </View>
  );
};

const mapStateToProps: MapStateToProps<ILoginState, ILoginBaseProps, IState> = (
  state: IState,
): ILoginState => ({ ...state.login });

const mapDispatchToProps: MapDispatchToProps<ILoginDispatchProps, ILoginBaseProps> = (
  dispatch: ThunkDispatcher,
): ILoginDispatchProps => ({
  onGoogleLogin: (): void => { dispatch(actions.performAsyncGoogleLogin()); },
});

const connectedLoginView: ConnectedComponentClass<React.FunctionComponent<ILoginProps>, ILoginBaseProps> = connect(
  mapStateToProps, mapDispatchToProps,
)(loginView);

export { connectedLoginView as LoginView };
