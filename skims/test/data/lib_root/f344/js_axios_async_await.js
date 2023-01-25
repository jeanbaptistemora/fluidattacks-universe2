const axiosAlias = require("axios");
import kyAlias from "ky";

const getData = async () => {
  //Should fail line 6
  const axiosResponse = await axiosAlias.get(`https://example.com`);
  localStorage.setItem("axiosKey", axiosResponse);
  localStorage.setItem("axiosKey", axiosResponse.method);

  //Should fail line 10
  const fetchResponse = await fetch("/movies");
  localStorage.setItem("fetchKey", fetchResponse);

  //Should fail line 10
  const kyResponse = await kyAlias("/movies");
  localStorage.setItem("fetchKey", kyResponse.whathever);

  //Shouldn't fail
  const safeVar = await otherFunction("/example");
  localStorage.setItem("safe", safeVar);
};
