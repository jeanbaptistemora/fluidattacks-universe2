import { StyleSheet } from "react-native";

export const styles: Record<
  string,
  // eslint-disable-next-line @typescript-eslint/ban-types
  StyleSheet.NamedStyles<{}>
> = StyleSheet.create({
  container: {
    alignItems: "center",
    flexDirection: "row",
  },
  text: {
    color: "#808080",
  },
});
