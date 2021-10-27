// eslint-disable-next-line import/no-named-as-default
import Constants from "expo-constants";
import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
  button: {
    backgroundColor: "#FFFFFF",
    borderRadius: 2,
    elevation: 2,
    flexDirection: "row",
    paddingTop: -5,
    shadowOffset: { height: 1, width: 0 },
    shadowOpacity: 0.3,
    shadowRadius: 1,
  },
  buttonContainer: {
    alignItems: "flex-end",
    flex: 0,
    flexDirection: "row",
    justifyContent: "space-between",
    paddingTop: 5,
  },
  container: {
    alignItems: "stretch",
    flex: 1,
    justifyContent: "flex-start",
    paddingTop: Constants.statusBarHeight,
  },
  modalView: {
    alignItems: "stretch",
    borderRadius: 2,
    elevation: 6,
    flex: 1,
    flexDirection: "column",
    justifyContent: "flex-start",
    marginBottom: 40,
    marginHorizontal: 20,
    marginTop: 40,
    padding: 10,
    shadowColor: "gray",
    shadowOffset: {
      height: 3,
      width: 0,
    },
    shadowOpacity: 0.25,
    shadowRadius: 5,
  },
  text: {
    fontSize: 17,
    fontWeight: "700",
    marginHorizontal: 8,
    marginVertical: 8,
    textAlign: "left",
  },
});
