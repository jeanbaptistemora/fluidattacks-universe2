interface IProps {
  pathname: string;
  crumbLabel: string;
}

export const capitalizeCrumbs = (crumbs: IProps[]): IProps[] => {
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
