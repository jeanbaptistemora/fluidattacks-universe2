import { Constants } from "expo";
import React from "react";
import { Image, Linking, Platform, View } from "react-native";
import { Button, Dialog, Paragraph, Portal } from "react-native-paper";
import { connect, ConnectedComponentClass, MapDispatchToProps, MapStateToProps } from "react-redux";
import { RedirectProps } from "react-router";
import { Redirect, RouteComponentProps } from "react-router-native";
import { InferableComponentEnhancer, lifecycle } from "recompose";

// tslint:disable-next-line: no-default-import
import { default as FluidLogo } from "../../../assets/logo.png";
import { Preloader } from "../../components/Preloader";
import { IState, ThunkDispatcher } from "../../store";
import { translate } from "../../utils/translations/translate";
import { checkVersion } from "../../utils/version";

import * as actions from "./actions";
import { ILoginState } from "./reducer";
import { styles } from "./styles";

type ILoginBaseProps = RouteComponentProps;

/**
 * Redux actions dispatched from LoginView
 */
interface ILoginDispatchProps {
  onGoogleLogin(): void;
  onResolveVersion(isOutdated: boolean): void;
}

export type ILoginProps = ILoginBaseProps & (ILoginState & ILoginDispatchProps);

const androidManifest: typeof Constants.manifest["android"] =
  Constants.manifest.android === undefined ? {} : Constants.manifest.android;

const enhance: InferableComponentEnhancer<{}> = lifecycle<ILoginProps, {}>({
  componentDidMount(): void {
    const { onResolveVersion } = this.props;

    checkVersion()
      .then((isOutdated: boolean): void => {
        const shouldSkipCheck: boolean = Platform.OS === "ios" || __DEV__;

        onResolveVersion(shouldSkipCheck ? false : isOutdated);
      })
      .catch();
  },
});

export const loginView: React.FunctionComponent<ILoginProps> = (props: ILoginProps): JSX.Element => {
  const handleGoogleButtonClick: (() => void) = (): void => { props.onGoogleLogin(); };

  const { t } = translate;

  const redirectParams: RedirectProps["to"] = {
    pathname: "/Welcome",
    state: {
      authProvider: props.authProvider,
      authToken: props.authToken,
      pushToken: props.pushToken,
      userInfo: props.userInfo,
    },
  };

  const handleUpdateButtonClick: (() => Promise<void>) = async (): Promise<void> => {
    await Linking.openURL(`market://details?id=${androidManifest.package}`);
  };

  return props.isAuthenticated ? <Redirect to={redirectParams} /> : (
    <View style={styles.container}>
      <Image source={FluidLogo} style={styles.logo} />
      <View style={styles.buttonsContainer}>
        <Button
          disabled={props.isLoading || props.isOutdated !== false}
          mode="contained"
          onPress={handleGoogleButtonClick}
        >
          {t(props.isLoading ? "login.authLoadingText" : "login.btnGoogleText")}
        </Button>
      </View>
      <Portal>
        <Dialog dismissable={false} visible={props.isOutdated === true}>
          <Dialog.Title>{t("login.newVersion.title")}</Dialog.Title>
          <Dialog.Content>
            <Paragraph>{t("login.newVersion.content")}</Paragraph>
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={handleUpdateButtonClick}>{t("login.newVersion.btn")}</Button>
          </Dialog.Actions>
        </Dialog>
      </Portal>
      <Preloader visible={props.isLoading} />
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
  onResolveVersion: (isOutdated: boolean): void => { dispatch(actions.resolveVersion(isOutdated)); },
});

const connectedLoginView: ConnectedComponentClass<React.ComponentClass<ILoginProps>, ILoginBaseProps> = connect(
  mapStateToProps, mapDispatchToProps,
)(enhance(loginView));

export { connectedLoginView as LoginView };
