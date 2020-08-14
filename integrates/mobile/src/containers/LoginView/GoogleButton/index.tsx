import React from "react";
import { useTranslation } from "react-i18next";
import { Image, Text, TouchableOpacity } from "react-native";

// tslint:disable-next-line: no-default-import
import { default as GoogleLogo } from "../../../../assets/google-logo.png";

import { styles } from "./styles";

/**
 * Google Sign In button
 * @see https://developers.google.com/identity/branding-guidelines
 */
export interface IGoogleButtonProps {
  disabled?: boolean;
  onPress(): void;
}

const googleButton: React.FC<IGoogleButtonProps> = (props: IGoogleButtonProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <TouchableOpacity
        style={[styles.container, props.disabled === true ? styles.disabled : undefined]}
        {...props}
      >
        <Image source={GoogleLogo} style={styles.icon} />
        <Text style={styles.label}>{t("login.btnGoogleText")}</Text>
      </TouchableOpacity>
    </React.StrictMode>
  );
};

export { googleButton as GoogleButton };
