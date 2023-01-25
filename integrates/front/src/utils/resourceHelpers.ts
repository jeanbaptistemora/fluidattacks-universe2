import _ from "lodash";

export const openUrl: (url: string, openANewTab?: boolean) => void = (
  url: string,
  openANewTab: boolean = true
): void => {
  const newTab: Window | null = window.open(
    url,
    openANewTab ? undefined : "_self",
    "noopener,noreferrer,"
  );
  if (_.isObject(newTab)) {
    // It is necessary to assign null to opener
    // eslint-disable-next-line fp/no-mutation
    newTab.opener = null;
  }
};
