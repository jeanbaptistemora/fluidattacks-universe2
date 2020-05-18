import { StyleSheet } from "react-native";

export const styles: Dictionary = StyleSheet.create({
  bottom: {
    flex: 1,
    justifyContent: "flex-end",
  },
  container: {
    backgroundColor: "#272727",
    flex: 1,
    flexDirection: "column",
    paddingTop: 50,
  },
  logo: {
    height: 80,
    marginLeft: 5,
    resizeMode: "stretch",
    width: 180,
  },
});
