export const timeFromNow: (value: string) => string = (
  value: string
): string => {
  const date = new Date(value);

  if (isNaN(date.getTime())) return "-";

  const dateDiff = new Date().getTime() - date.getTime();

  switch (true) {
    case dateDiff < 60000:
      return `${Math.floor(dateDiff / 1000)} seconds ago`;

    case dateDiff < 60000 * 60:
      return `${Math.floor(dateDiff / 60000)} minutes ago`;

    case dateDiff < 60000 * 60 * 24:
      return `${Math.floor(dateDiff / (60000 * 60))} hours ago`;

    case dateDiff < 60000 * 60 * 24 * 30:
      return `${Math.floor(dateDiff / (60000 * 60 * 24))} days ago`;

    case dateDiff < 60000 * 60 * 24 * 30 * 12:
      return `${Math.floor(dateDiff / (60000 * 60 * 24 * 30))} months ago`;

    default:
      return `${Math.floor(dateDiff / (60000 * 60 * 24 * 30 * 12))} years ago`;
  }
};
