// Needed to override styles
/* eslint-disable react/forbid-component-props */
import type { ApolloError } from "@apollo/client";
import { useMutation } from "@apollo/client";
import { FontAwesome5 } from "@expo/vector-icons";
import type { GraphQLError } from "graphql";
import React, { useCallback, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  Alert,
  Modal,
  Text,
  TouchableOpacity,
  View,
  useWindowDimensions,
} from "react-native";
import { Avatar as PaperAvatar, useTheme } from "react-native-paper";
import { useHistory } from "react-router-native";

import { REMOVE_ACCOUNT_MUTATION } from "./queries";
import { styles } from "./styles";
import type { IRemoveAccountResult } from "./types";

import { LOGGER } from "../../utils/logger";
import { useSessionToken } from "../../utils/sessionToken/context";
import type { IAuthState } from "../../utils/socialAuth";
import { logout } from "../../utils/socialAuth";

/** User avatar */
interface IAvatarProps {
  photoUrl?: string; // eslint-disable-line react/require-default-props
  size: number;
  userName: string;
}

const maxInitials: number = 2;
const getInitials: (name: string) => string = (name: string): string =>
  // eslint-disable-next-line fp/no-mutating-methods
  name
    .split(" ")
    .splice(0, maxInitials)
    .map((word: string): string => word.charAt(0).toUpperCase())
    .join("");

const Avatar: React.FC<IAvatarProps> = ({
  photoUrl,
  size,
  userName,
}: IAvatarProps): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { colors } = useTheme();
  const { t } = useTranslation();
  const { height, width } = useWindowDimensions();
  const { user } = history.location.state as IAuthState;
  const [visible, setVisible] = useState(false);
  const [, setSessionToken] = useSessionToken();
  const AvatarModal: React.MutableRefObject<TouchableOpacity | null> =
    useRef(null);
  const [dropdownTop, setDropdownTop] = useState(0);
  const [removeAccount, { client }] = useMutation(REMOVE_ACCOUNT_MUTATION, {
    onCompleted: async (mtResult: IRemoveAccountResult): Promise<void> => {
      if (mtResult.removeStakeholder.success) {
        client.stop();
        await client.clearStore();
        await logout(setSessionToken);
        history.replace("/Login");
      } else {
        history.replace("/Dashboard", { user });
      }
    },
    onError: (removeError: ApolloError): void => {
      removeError.graphQLErrors.forEach((error: GraphQLError): void => {
        LOGGER.error("An error occurred while deleting account", error);
      });
      history.replace("/Dashboard", { user });
    },
  });

  const openDropdown = useCallback((): void => {
    const topValue = 5;
    AvatarModal.current?.measure(
      (_fx, _fy, _w, modalHeight, _px, pageY): void => {
        setDropdownTop(pageY + modalHeight - topValue);
      }
    );
    setVisible(true);
  }, []);

  const toggleDropdown = useCallback((): void => {
    if (visible) {
      setVisible(false);
    } else {
      openDropdown();
    }
  }, [openDropdown, visible]);

  const onItemPress = useCallback((): void => {
    setVisible(false);
  }, []);

  const displayDialog: () => void = useCallback((): void => {
    Alert.alert(
      t("avatar.alert.title"),
      `\n${t("avatar.alert.warning.text")}\n${t(
        "avatar.alert.warning.secondText"
      )}\n${t("avatar.alert.warning.firstText")}\n`,
      [
        {
          onPress: (): void => {
            setVisible(false);
          },
          text: t("avatar.alert.buttons.cancel"),
        },
        {
          onPress: async (): Promise<void> => {
            setVisible(false);
            await removeAccount();
          },
          text: t("avatar.alert.buttons.continue"),
        },
      ],
      { cancelable: false }
    );
  }, [t, removeAccount]);

  const onDeletePress = useCallback((): void => {
    displayDialog();
  }, [displayDialog]);

  return (
    <React.StrictMode>
      <TouchableOpacity onPress={toggleDropdown} ref={AvatarModal}>
        {photoUrl === undefined ? (
          <PaperAvatar.Text label={getInitials(userName)} size={size} />
        ) : (
          <PaperAvatar.Image size={size} source={{ uri: photoUrl }} />
        )}
        <Modal animationType={"none"} transparent={true} visible={visible}>
          <TouchableOpacity onPress={onItemPress} style={styles.overlay}>
            <View
              style={[
                styles.modal,
                {
                  backgroundColor: colors.background,
                  maxHeight: height,
                  maxWidth: width,
                  top: dropdownTop,
                },
              ]}
            >
              <TouchableOpacity onPress={onDeletePress} style={styles.item}>
                <FontAwesome5 color={"#DB4437"} name={"trash-alt"} size={24} />
                <Text style={[styles.text, { color: colors.text }]}>
                  {" Delete Account"}
                </Text>
              </TouchableOpacity>
            </View>
          </TouchableOpacity>
        </Modal>
      </TouchableOpacity>
    </React.StrictMode>
  );
};

export { Avatar };
