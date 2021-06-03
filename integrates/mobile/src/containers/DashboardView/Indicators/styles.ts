import { Dimensions, StyleSheet } from "react-native";

export const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    width: Dimensions.get("window").width,
  },
  diff: {
    alignItems: "center",
    flexDirection: "row",
  },
  percentageContainer: {
    alignItems: "center",
    justifyContent: "center",
    marginTop: 10,
  },
  percentageText: {
    fontSize: 30,
    position: "absolute",
  },
  remediatedText: {
    fontWeight: "bold",
    marginTop: 15,
  },
  remediationContainer: {
    alignItems: "center",
    marginTop: 8,
  },
});
