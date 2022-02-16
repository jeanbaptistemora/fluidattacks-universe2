import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
  item: {
    alignItems: "center",
    borderBottomWidth: 1,
    flexDirection: "row",
    paddingHorizontal: 10,
    paddingVertical: 15,
  },
  modal: {
    shadowColor: "#000000",
    shadowOffset: { height: 4, width: 0 },
    shadowOpacity: 0.5,
    shadowRadius: 4,
    width: "100%",
  },
  overlay: {
    height: "100%",
    width: "100%",
  },
  text: {
    textAlign: "left",
  },
});
