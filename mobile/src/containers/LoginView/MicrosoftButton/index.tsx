import React from "react";
import { useTranslation } from "react-i18next";
import { Image, Text, TouchableOpacity } from "react-native";

// tslint:disable-next-line: no-default-import
import { default as MicrosoftLogo } from "../../../../assets/microsoft-logo.png";

import { styles } from "./styles";

/**
 * Microsoft Sign In button
 * @see https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-add-branding-in-azure-ad-apps
 */
export interface IMicrosoftButtonProps {
  disabled?: boolean;
  onPress(): void;
}

const microsoftButton: React.FC<IMicrosoftButtonProps> = (props: IMicrosoftButtonProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <TouchableOpacity
        style={[styles.container, props.disabled === true ? styles.disabled : undefined]}
        {...props}
      >
        <Image source={MicrosoftLogo} style={styles.icon} />
        <Text style={styles.label}>{t("login.btnMicrosoftText")}</Text>
      </TouchableOpacity>
    </React.StrictMode>
  );
};

export { microsoftButton as MicrosoftButton };
