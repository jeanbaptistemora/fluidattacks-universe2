import React from "react";
import { Text, View } from "react-native";
import { RouteComponentProps } from "react-router-native";

import { styles } from "./styles";

interface IUser {
  email?: string;
  familyName: string;
  givenName: string;
  id: string;
  name: string;
  photoUrl?: string;
}

type IMenuProps = RouteComponentProps<{}, {}, { userInfo: IUser }>;

const menuView: React.FunctionComponent<IMenuProps> = (props: IMenuProps): JSX.Element => {
  const { userInfo } = props.location.state;

  return (
    <View style={styles.container}>
      <Text>Welcome {userInfo.givenName}!</Text>
    </View>
  );
};

export { menuView as MenuView };
