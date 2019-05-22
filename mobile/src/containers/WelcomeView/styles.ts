import { StyleSheet } from "react-native";

export const styles: Dictionary = StyleSheet.create({
  container: {
    alignContent: "center",
    backgroundColor: "#272727",
    flex: 1,
    flexDirection: "column",
    justifyContent: "center",
  },
  greeting: {
    color: "#ffffff",
    fontSize: 36,
    fontWeight: "700",
    textAlign: "center",
  },
  profilePicture: {
    alignSelf: "center",
    borderColor: "rgba(0,0,0,0.2)",
    borderRadius: 150,
    borderWidth: 3,
    height: 100,
    marginTop: 15,
    width: 100,
  },
});
