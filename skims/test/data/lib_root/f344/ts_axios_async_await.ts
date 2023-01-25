import axios from "axios";
import ky from "ky";

const getData = async () => {
  //Should fail line 6
  const axiosResponse = await axios.get(`https://example.com`);
  localStorage.setItem("axiosKey", axiosResponse);

  //Should fail line 10
  const fetchResponse = await fetch("/movies");
  localStorage.setItem("fetchKey", fetchResponse);

  //Should fail line 10
  const kyResponse = await ky("/movies");
  localStorage.setItem("fetchKey", kyResponse);

  //Shouldn't fail
  const safeVar = await otherFunction("/example");
  localStorage.setItem("safe", safeVar);
};
