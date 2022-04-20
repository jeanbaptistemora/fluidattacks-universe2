// Needed to override styles
/* eslint-disable react/forbid-component-props */
import React from "react";
import { useTranslation } from "react-i18next";
import { Image, Text, TouchableOpacity } from "react-native";

import { styles } from "./styles";

import GoogleLogo from "../../../../assets/google-logo.png";

/**
 * Google Sign In button
 * @see https://developers.google.com/identity/branding-guidelines
 */
interface IGoogleButtonProps {
  // Needed to avoid defaultProps mutations
  // eslint-disable-next-line react/require-default-props
  disabled?: boolean;
  onPress: () => void;
}

const GoogleButton: React.FC<IGoogleButtonProps> = (
  props: IGoogleButtonProps
): JSX.Element => {
  const { t } = useTranslation();
  const { disabled } = props;

  return (
    <React.StrictMode>
      <TouchableOpacity
        style={[
          styles.container,
          disabled === true ? styles.disabled : undefined,
        ]}
        // We need props spreading in order to pass down props to the button.
        // eslint-disable-next-line react/jsx-props-no-spreading
        {...props}
      >
        <Image source={GoogleLogo} style={styles.icon} />
        <Text style={styles.label}>{t("login.btnGoogleText")}</Text>
      </TouchableOpacity>
    </React.StrictMode>
  );
};

export type { IGoogleButtonProps };
export { GoogleButton };
