import React from "react";
import { useTranslation } from "react-i18next";
import { Image, Text, TouchableOpacity } from "react-native";

import {
  // tslint:disable-next-line: no-default-import
  default as BitbucketLogo,
} from "../../../../assets/bitbucket-logo.png";

import { styles } from "./styles";

/**
 * Bitbucket Sign In button
 * @see https://atlassian.design/foundations/
 */
export interface IBitbucketButtonProps {
  disabled?: boolean;
  onPress(): void;
}

const bitbucketButton: React.FC<IBitbucketButtonProps> = (
  props: IBitbucketButtonProps,
): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <TouchableOpacity
        style={[
          styles.container,
          props.disabled === true ? styles.disabled : undefined,
        ]}
        {...props}
      >
        <Image source={BitbucketLogo} style={styles.icon} />
        <Text style={styles.label}>{t("login.btnBitbucketText")}</Text>
      </TouchableOpacity>
    </React.StrictMode>
  );
};

export { bitbucketButton as BitbucketButton };
