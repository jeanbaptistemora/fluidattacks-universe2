// Needed to override styles
/* eslint-disable react/forbid-component-props */
import React from "react";
import { useTranslation } from "react-i18next";
import { Image, Text, TouchableOpacity } from "react-native";

import { styles } from "./styles";

import BitbucketLogo from "../../../../assets/bitbucket-logo.png";

/**
 * Bitbucket Sign In button
 * @see https://atlassian.design/foundations/
 */
interface IBitbucketButtonProps {
  // Needed to avoid defaultProps mutations
  // eslint-disable-next-line react/require-default-props
  disabled?: boolean;
  onPress: () => void;
}

const BitbucketButton: React.FC<IBitbucketButtonProps> = (
  props: IBitbucketButtonProps
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
        <Image source={BitbucketLogo} style={styles.icon} />
        <Text style={styles.label}>{t("login.btnBitbucketText")}</Text>
      </TouchableOpacity>
    </React.StrictMode>
  );
};

export type { IBitbucketButtonProps };
export { BitbucketButton };
