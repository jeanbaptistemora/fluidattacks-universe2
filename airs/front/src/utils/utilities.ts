interface IProps {
  pathname: string;
  crumbLabel: string;
}

const capitalizeObject = (crumbs: IProps[]): IProps[] => {
  const capitalizedCrumbs = crumbs.map(
    (crumb): IProps => {
      const properties = {
        crumbLabel: `${crumb.crumbLabel
          .charAt(0)
          .toUpperCase()}${crumb.crumbLabel.slice(1).replace("-", "")}`,
        pathname: crumb.pathname,
      };

      return properties;
    }
  );

  return capitalizedCrumbs;
};

const capitalizePlainString = (title: string): string => {
  const parsedTitle: string = `${title.charAt(0).toUpperCase()}${title.slice(
    1
  )}`;

  return parsedTitle;
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

export { capitalizeDashedString, capitalizeObject, capitalizePlainString };
