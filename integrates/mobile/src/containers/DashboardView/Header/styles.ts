// eslint-disable-next-line import/no-named-as-default
import Constants from "expo-constants";
import { StyleSheet } from "react-native";

export const styles: Record<
  string,
  Record<string, unknown>
> = StyleSheet.create({
  actions: {
    marginLeft: "auto",
  },
  avatar: {
    paddingRight: 10,
  },
  container: {
    alignItems: "center",
    elevation: 0,
    flexDirection: "row",
    height: 85,
    paddingHorizontal: 20,
    paddingTop: Constants.statusBarHeight,
  },
  email: {
    fontSize: 11,
  },
  logout: {
    color: "lightgray",
    fontWeight: "500",
    padding: 15,
    paddingRight: 0,
    textAlign: "right",
  },
  name: {
    fontSize: 17,
    fontWeight: "500",
  },
});
