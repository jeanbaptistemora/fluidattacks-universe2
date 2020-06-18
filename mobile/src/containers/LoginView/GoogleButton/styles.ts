import { StyleSheet } from "react-native";

export const styles: Dictionary = StyleSheet.create({
  container: {
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    borderRadius: 2,
    elevation: 2,
    flexDirection: "row",
    marginBottom: 10,
    shadowOffset: { height: 1, width: 0 },
    shadowOpacity: 0.3,
    shadowRadius: 1,
  },
  disabled: {
    backgroundColor: "#BDBDBD",
    elevation: 0,
  },
  icon: {
    height: 21,
    marginLeft: 12,
    resizeMode: "contain",
    width: 21,
  },
  label: {
    color: "#757575",
    fontSize: 14,
    marginHorizontal: 12,
    marginVertical: 9,
    textAlign: "center",
  },
});
