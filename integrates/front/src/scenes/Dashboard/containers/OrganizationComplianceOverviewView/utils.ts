import _ from "lodash";

const PERCENTAGE_BASE = 100;

const handleCompliancePercentageValue: (value: number | null) => number = (
  value: number | null
): number => (_.isNull(value) ? 0 : Math.round(value * PERCENTAGE_BASE));

const handleComplianceValue: (value: number | null) => number = (
  value: number | null
): number => (_.isNull(value) ? 0.0 : value);

const getProgressBarColor: (progress: number) => string = (
  progress: number
): string => {
  const LOW_PROGRESS_LIMIT = 30;
  const MEDIUM_PROGRESS_LIMIT = 70;
  if (progress <= LOW_PROGRESS_LIMIT) {
    return "#BF0B1A";
  } else if (progress <= MEDIUM_PROGRESS_LIMIT) {
    return "#FF961E";
  }

  return "#009245";
};

export {
  getProgressBarColor,
  handleCompliancePercentageValue,
  handleComplianceValue,
};
