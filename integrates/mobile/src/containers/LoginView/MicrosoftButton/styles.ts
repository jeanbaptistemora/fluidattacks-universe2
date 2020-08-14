import { StyleSheet } from "react-native";

export const styles: Dictionary = StyleSheet.create({
  container: {
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    borderColor: "#8C8C8C",
    borderWidth: 1,
    flexDirection: "row",
    marginBottom: 10,
  },
  disabled: {
    backgroundColor: "#BDBDBD",
  },
  icon: {
    height: 21,
    marginLeft: 12,
    width: 21,
  },
  label: {
    color: "#5E5E5E",
    fontSize: 14,
    marginHorizontal: 12,
    marginVertical: 9,
    textAlign: "center",
  },
});
