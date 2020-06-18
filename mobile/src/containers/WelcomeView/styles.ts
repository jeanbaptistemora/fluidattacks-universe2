import { StyleSheet } from "react-native";

export const styles: Dictionary = StyleSheet.create({
  container: {
    alignContent: "center",
    flex: 1,
    flexDirection: "column",
    justifyContent: "center",
  },
  greeting: {
    fontSize: 36,
    fontWeight: "700",
    textAlign: "center",
  },
  profilePicture: {
    alignSelf: "center",
    borderColor: "rgba(0,0,0,0.2)",
    borderRadius: 60,
    borderWidth: 3,
    marginTop: 15,
  },
});
