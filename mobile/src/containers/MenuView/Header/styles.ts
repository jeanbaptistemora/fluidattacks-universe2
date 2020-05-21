import { default as Constants } from "expo-constants";
import { StyleSheet } from "react-native";

export const styles: Dictionary = StyleSheet.create({
  actions: {
    marginLeft: "auto",
  },
  avatar: {
    paddingRight: 10,
  },
  container: {
    alignItems: "center",
    elevation: 4,
    flexDirection: "row",
    height: 80,
    paddingHorizontal: 20,
    paddingTop: Constants.statusBarHeight,
  },
  greeting: {
    fontWeight: "500",
  },
  logout: {
    color: "lightgray",
    fontWeight: "500",
  },
});
