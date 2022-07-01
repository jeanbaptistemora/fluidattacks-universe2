import { Logger } from "utils/logger";

interface ICountries {
  currency: string;
  currency_name: string;
  emojiU: string;
  id: number;
  name: string;
  phone_code: number;
  states: {
    cities: {
      id: number;
      name: string;
    }[];
    id: number;
    name: string;
  }[];
}

const countries = async (
  setCities: React.Dispatch<React.SetStateAction<ICountries[] | undefined>>
): Promise<void> => {
  const url =
    "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/countries%2Bstates%2Bcities.json";
  const errorMsg = "Couldn't fetch countries, states and cities database";

  try {
    const response = await fetch(url);

    if (response.status === 200) {
      const citiesObj: ICountries[] = await response.json();
      setCities(citiesObj);
    } else {
      Logger.error(errorMsg, response);
      setCities(undefined);
    }
  } catch (error) {
    Logger.error(errorMsg, error);
    setCities(undefined);
  }
};

export { countries };
export type { ICountries };
