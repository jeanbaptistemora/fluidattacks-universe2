/* eslint require-unicode-regexp:0 */

interface IProps {
  pathname: string;
  crumbLabel: string;
}

const capitalizePlainString = (title: string): string => {
  return `${title.charAt(0).toUpperCase()}${title.slice(1).replace("-", "")}`;
};

const capitalizeDashedString: (words: string) => string = (
  words: string
): string => {
  const separateWord = words.toLowerCase().split("-");

  const capitalizedName = separateWord.map(
    (word: string): string =>
      `${word.charAt(0).toUpperCase()}${word.substring(1)}`
  );

  return capitalizedName.join(" ");
};

const capitalizeObject = (crumbs: IProps[]): IProps[] => {
  return crumbs.map(
    (crumb): IProps => {
      return {
        crumbLabel: capitalizeDashedString(crumb.crumbLabel),
        pathname: crumb.pathname,
      };
    }
  );
};

const stringToUri = (word: string): string => {
  return word
    .toLowerCase()
    .replace(" ", "-")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
};

const countCoincidences: (word: string, wordList: string[]) => number = (
  word: string,
  wordList: string[]
): number => {
  return wordList.filter((item): boolean => item === word).length;
};

export {
  capitalizeDashedString,
  capitalizeObject,
  capitalizePlainString,
  countCoincidences,
  stringToUri,
};
