import { StyleSheet } from "react-native";

export const styles: Record<
  string, Record<string, unknown>
> = StyleSheet.create({
  container: {
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    flexDirection: "row",
    marginBottom: 10,
  },
  disabled: {
    backgroundColor: "#BDBDBD",
  },
  icon: {
    height: 26,
    marginLeft: 10,
    width: 26,
  },
  label: {
    color: "#172B4D",
    fontSize: 14,
    marginHorizontal: 10,
    marginVertical: 9,
    textAlign: "center",
  },
});
