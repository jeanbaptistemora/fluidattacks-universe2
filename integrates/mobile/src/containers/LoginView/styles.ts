import { StyleSheet } from "react-native";

export const styles: Record<
  string, Record<string, unknown>
> = StyleSheet.create({
  bottom: {
    alignItems: "center",
    flex: 1,
    justifyContent: "flex-end",
    marginBottom: 15,
  },
  buttonsContainer: {
    marginTop: 125,
  },
  container: {
    alignItems: "center",
    flex: 1,
    flexDirection: "column",
    paddingTop: 100,
  },
});
