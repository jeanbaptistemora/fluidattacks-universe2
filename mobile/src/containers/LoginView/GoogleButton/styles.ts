import { StyleSheet } from "react-native";

export const styles: Dictionary = StyleSheet.create({
  container: {
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    borderRadius: 1,
    elevation: 1,
    flexDirection: "row",
    justifyContent: "center",
    marginBottom: 10,
  },
  disabled: {
    backgroundColor: "#BDBDBD",
    elevation: 0,
  },
  icon: {
    height: 18,
    marginLeft: 12,
    width: 18,
  },
  label: {
    color: "#757575",
    fontSize: 14,
    fontWeight: "600",
    marginHorizontal: 12,
    marginVertical: 9,
    textAlign: "center",
  },
});
