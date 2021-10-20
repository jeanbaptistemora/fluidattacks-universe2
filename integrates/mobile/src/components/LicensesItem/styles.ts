import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
  card: {
    alignItems: "center",
    borderRadius: 4,
    flexDirection: "row",
    overflow: "hidden",
  },
  cardShadow: {
    borderRadius: 2,
    elevation: 0,
    marginHorizontal: 6,
    marginVertical: 3,
    shadowColor: "lightgray",
    shadowOffset: { height: 0, width: 0 },
    shadowOpacity: 0.05,
    shadowRadius: 0.3,
  },
  item: {
    backgroundColor: "transparent",
    flex: 1,
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
    paddingHorizontal: 6,
    paddingVertical: 3,
  },
  name: {
    fontSize: 16,
    fontWeight: "500",
  },
  text: {
    marginTop: 3,
  },
});
