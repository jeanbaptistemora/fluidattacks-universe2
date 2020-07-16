import { StyleSheet } from "react-native";

export const styles: Dictionary = StyleSheet.create({
  bottom: {
    alignItems: "center",
    flex: 1,
    justifyContent: "flex-end",
    marginBottom: 15,
  },
  container: {
    alignItems: "center",
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
    marginTop: 20,
  },
  remediationContainer: {
    alignItems: "center",
    marginTop: 15,
  },
});
