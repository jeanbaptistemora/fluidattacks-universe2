const axios = require("axios");

// Make a request for a user with a given ID
axios.get("/user?ID=12345").then(function (response) {
  localStorage.setItem("sensData", response);
});

// Optionally the request above could also be done as
axios
  .get("/user", {
    params: {
      ID: 12345,
    },
  })
  .then(function (res) {
    localStorage.setItem("sensDataII", res);
  });

// async/await implementation
async function getUser() {
  try {
    const responseIII = await axios.get("/user?ID=12345");
    localStorage.setItem("sensDataIII", responseIII);
  } catch (error) {
    console.error(error);
  }
}
