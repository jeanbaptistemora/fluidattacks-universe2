/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
  setCountries: React.Dispatch<React.SetStateAction<ICountries[] | undefined>>
): Promise<void> => {
  const url =
    "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/countries%2Bstates%2Bcities.json";
  const errorMsg = "Couldn't fetch countries, states and cities database";

  try {
    const response = await fetch(url);

    if (response.status === 200) {
      const countriesObj: ICountries[] = await response.json();
      setCountries(countriesObj);
    } else {
      Logger.error(errorMsg, response);
      setCountries(undefined);
    }
  } catch (error) {
    Logger.error(errorMsg, error);
    setCountries(undefined);
  }
};

export { countries };
export type { ICountries };
