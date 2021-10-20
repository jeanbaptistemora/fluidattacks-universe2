// Needed to override styles
/* eslint-disable react/forbid-component-props */
import React from "react";
import type { StyleProp, TextStyle } from "react-native";
import { Linking, Text, TouchableOpacity } from "react-native";

interface ILink {
  // eslint-disable-next-line react/require-default-props
  url?: string;
  style: StyleProp<TextStyle>;
  children: React.ReactNode;
}

export const Link: React.FC<ILink> = ({
  children,
  style,
  url,
}: ILink): JSX.Element => {
  async function handlePress(): Promise<void> {
    if (url !== undefined) {
      await Linking.openURL(url);
    }
  }

  return (
    <TouchableOpacity onPress={handlePress}>
      <Text numberOfLines={1} onPress={handlePress} style={style}>
        {children}
      </Text>
    </TouchableOpacity>
  );
};
