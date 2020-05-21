import { StyleSheet } from "react-native";

export const styles: Dictionary = StyleSheet.create({
  bottom: {
    flex: 1,
    justifyContent: "flex-end",
    marginBottom: 15,
  },
  container: {
    flex: 1,
    flexDirection: "column",
    paddingHorizontal: 10,
    paddingTop: 30,
  },
  percentageContainer: {
    alignItems: "center",
    justifyContent: "center",
  },
  percentageText: {
    fontSize: 30,
    position: "absolute",
  },
  remediatedText: {
    fontWeight: "bold",
  },
  remediationContainer: {
    alignItems: "center",
    marginTop: 20,
  },
});
