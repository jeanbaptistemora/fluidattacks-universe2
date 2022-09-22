/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Logger } from "utils/logger";

interface ICountry {
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

const getCountries = async (): Promise<ICountry[]> => {
  const url =
    "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/countries%2Bstates%2Bcities.json";
  const errorMsg = "Couldn't fetch countries, states and cities database";

  try {
    const response = await fetch(url);

    if (response.status === 200) {
      const countries: ICountry[] = await response.json();

      return countries;
    }
    Logger.error(errorMsg, response);

    return [];
  } catch (error) {
    Logger.error(errorMsg, error);

    return [];
  }
};

export { getCountries };
export type { ICountry };
