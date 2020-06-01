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
    borderRadius: 50,
    borderWidth: 3,
    marginTop: 15,
  },
  unauthorized: {
    color: "#ffffff",
    fontSize: 16,
    margin: 6,
    textAlign: "center",
  },
});
