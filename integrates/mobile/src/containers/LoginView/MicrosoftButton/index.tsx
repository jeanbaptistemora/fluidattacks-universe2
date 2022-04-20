// Needed to override styles
/* eslint-disable react/forbid-component-props */
import React from "react";
import { useTranslation } from "react-i18next";
import { Image, Text, TouchableOpacity } from "react-native";

import { styles } from "./styles";

import MicrosoftLogo from "../../../../assets/microsoft-logo.png";

/**
 * Microsoft Sign In button
 * @see https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-add-branding-in-azure-ad-apps
 */
interface IMicrosoftButtonProps {
  // Needed to avoid defaultProps mutations
  // eslint-disable-next-line react/require-default-props
  disabled?: boolean;
  onPress: () => void;
}

const MicrosoftButton: React.FC<IMicrosoftButtonProps> = (
  props: IMicrosoftButtonProps
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
        <Image source={MicrosoftLogo} style={styles.icon} />
        <Text style={styles.label}>{t("login.btnMicrosoftText")}</Text>
      </TouchableOpacity>
    </React.StrictMode>
  );
};

export type { IMicrosoftButtonProps };
export { MicrosoftButton };
