import { StyleSheet } from "react-native";

export const styles: Record<
  string, Record<string, unknown>
> = StyleSheet.create({
  container: {
    alignItems: "center",
  },
  loadingGif: {
    height: 70,
    resizeMode: "stretch",
    width: 70,
  },
});
