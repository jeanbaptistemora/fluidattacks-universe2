import type { Dayjs } from "dayjs";
import dayjs, { extend, isDayjs } from "dayjs";
import isBetween from "dayjs/plugin/isBetween";
import isSameOrBefore from "dayjs/plugin/isSameOrBefore";
import _ from "lodash";
import {
  hasLengthGreaterThan,
  hasLengthLessThan,
  isAlphaNumeric,
  isNumeric,
  isRequired,
  matchesPattern,
} from "revalidate";

import type { IPhoneData } from "./forms/fields/PhoneNumber/FormikPhone/types";

import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

const regExps = {
  alphabetic: /^[a-zA-Z]+$/u,
  alphanumeric: /^[a-zA-Z0-9]+$/u,
  commitHash: /^[A-Fa-f0-9]{40}$|^[A-Fa-f0-9]{64}$/u,
  numeric: /^\d+$/u,
  text: /^[\w\-\s,;.¿?¡!]+$/u,
  vulnerabilityWhere: /^[^=/]+.+$/u,
};

/**
 * Groups single or multiple field-level validations and returns the first error
 *
 * Example: composeValidators([val1, val2, val3])
 */

// Needed for compatibility with all kind of validators
// eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-type-alias
type Validator = (value: any, allValues?: any, props?: any, name?: any) => any;

const composeValidators =
  (
    // Needed for compatibility with ConfigurableValidator parameters
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    args: ((value: any) => string | undefined)[]
  ): ((value: unknown) => string | undefined) =>
  (value: unknown): string | undefined => {
    const errors = args
      .map((validator): string | undefined => validator(value))
      .filter((error): boolean => error !== undefined);

    return errors[0];
  };

const required: Validator = isRequired({
  message: translate.t("validations.required"),
});

const getGroupValues: (
  allValues: Record<string, Record<string, unknown>>,
  name: string
) => Record<string, unknown> | undefined = (
  allValues: Record<string, Record<string, unknown>>,
  name: string
): Record<string, unknown> | undefined => {
  const fieldId: string[] = name.split(".");

  if (fieldId.length > 1) {
    const [groupName] = fieldId;

    return allValues[groupName];
  }
  Logger.error(
    `Fields must be grouped by a <FormSection> component`,
    new TypeError(
      `Field ${fieldId.toString()} must be grouped by a <FormSection> component`
    )
  );

  return undefined;
};

const someRequired: Validator = (
  _0: boolean,
  allValues: Record<string, Record<string, unknown>>,
  _1: Record<string, unknown>,
  name: string
): string | undefined => {
  const groupValues: Record<string, unknown> | undefined = getGroupValues(
    allValues,
    name
  );
  const isValid: boolean = _.some(groupValues);

  return isValid ? undefined : translate.t("validations.someRequired");
};

function checkIfValid(
  hasDescription: boolean,
  hasUrl: boolean,
  hasFileSelected: boolean
): string | undefined {
  if (hasDescription) {
    if (hasUrl) {
      return undefined;
    }

    return hasFileSelected
      ? undefined
      : translate.t("groupAlerts.noFileSelected");
  }

  return hasFileSelected ? translate.t("validations.required") : undefined;
}

const isValidEvidenceDescription: (
  url: string | undefined,
  file: object | undefined
) => Validator =
  (url: string | undefined, file: object | undefined): Validator =>
  (value: string | undefined): string | undefined => {
    const hasUrl: boolean = url !== "";
    const hasDescription: boolean = value !== "";
    const hasFileSelected: boolean = file !== undefined;

    return checkIfValid(hasDescription, hasUrl, hasFileSelected);
  };

const validTextField: Validator = (value: string): string | undefined => {
  if (!_.isNil(value)) {
    const beginTextMatch: RegExpMatchArray | null = /^=/u.exec(value);
    if (!_.isNull(beginTextMatch)) {
      return translate.t("validations.invalidTextBeginning", {
        chars: `'${beginTextMatch[0]}'`,
      });
    }

    const textMatch: RegExpMatchArray | null =
      // We use them for control character pattern matching.
      // eslint-disable-next-line no-control-regex
      /[^a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s(){}[\],./:;@&_$%'#*=?!+-]/u.exec(
        value
      );
    if (!_.isNull(textMatch)) {
      return translate.t("validations.invalidTextField", {
        chars: `'${textMatch[0]}'`,
      });
    }

    return undefined;
  }

  return undefined;
};

const validCsvInput: Validator = (value: string): string | undefined => {
  if (!_.isNil(value)) {
    const beginTextMatch: RegExpMatchArray | null =
      /^=|^-|^\+|^@|^\t|^\r/u.exec(value);
    if (!_.isNull(beginTextMatch)) {
      return translate.t("validations.invalidTextBeginning", {
        chars: `'${beginTextMatch[0]}'`,
      });
    }

    const contentTextMatch: RegExpMatchArray | null =
      /["',;](?:[-=+@\t\r])/u.exec(value);
    if (!_.isNull(contentTextMatch)) {
      return translate.t("validations.invalidTextPattern", {
        chars: `'${contentTextMatch[0]}'`,
      });
    }
  }

  return undefined;
};

const validUrlField: (value: string) => string | undefined = (
  value: string
): string | undefined => {
  if (_.isNil(value)) {
    return undefined;
  }

  const encodedCharWhitelist: string[] = ["%20"];

  const cleanValue: string = encodedCharWhitelist.reduce(
    (valueBeingCleaned: string, encodedChar: string): string =>
      valueBeingCleaned.replace(new RegExp(encodedChar, "gu"), ""),
    value
  );
  if (!_.isNil(cleanValue)) {
    const textMatch: RegExpMatchArray | null = /^=/u.exec(value);
    if (!_.isNull(textMatch)) {
      return translate.t("validations.invalidTextBeginning", {
        chars: `'${textMatch[0]}'`,
      });
    }

    const urlMatch: RegExpMatchArray | null =
      /[^a-zA-Z0-9(),./:;@_$#=?-]/u.exec(cleanValue);
    if (!_.isNull(urlMatch)) {
      return translate.t("validations.invalidUrlField", {
        chars: `'${urlMatch[0]}'`,
      });
    }

    return undefined;
  }

  return undefined;
};

const numberBetween: (min: number, max: number) => Validator =
  (min: number, max: number): Validator =>
  (value: number): string | undefined =>
    value < min || value > max
      ? translate.t("validations.between", { max, min })
      : undefined;

const optionalNumberBetween: (min: number, max: number) => Validator =
  (min: number, max: number): Validator =>
  (value: number | string): string | undefined =>
    _.isNumber(value) && (value < min || value > max)
      ? translate.t("validations.between", { max, min })
      : undefined;

const isPositive = (value: number): string | undefined =>
  value < 0 ? translate.t("validations.positive") : undefined;

const isZeroOrPositive = (value: number): string | undefined =>
  value < 0 ? translate.t("validations.zeroOrPositive") : undefined;

const minLength: (min: number) => Validator = (min: number): Validator =>
  hasLengthGreaterThan(min - 1)({
    message: translate.t("validations.minLength", { count: min }),
  }) as Validator;

const maxLength: (max: number) => Validator = (max: number): Validator =>
  hasLengthLessThan(max)({
    message: translate.t("validations.maxLength", { count: max }),
  }) as Validator;

const sameValue =
  (groupName: string): Validator =>
  (value: string): string | undefined =>
    value === groupName ? undefined : translate.t("validations.required");

const numeric: Validator = isNumeric({
  message: translate.t("validations.numeric"),
});

const alphaNumeric: Validator = isAlphaNumeric({
  message: translate.t("validations.alphanumeric"),
});

const validAlphanumericSpace: Validator = matchesPattern(/^[a-z\d\s]+$/iu)({
  message: translate.t("validations.alphanumeric"),
});

const validEmail: Validator = matchesPattern(
  /^[a-zA-Z0-9.!#$%&’*/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/u
)({
  message: translate.t("validations.email"),
});

const validCommitHash: Validator = matchesPattern(
  /^[A-Fa-f0-9]{40}$|^[A-Fa-f0-9]{64}$/u
)({
  message: translate.t("validations.commitHash"),
});

const validDraftTitle: (title: string) => string | undefined = (
  title: string
): string | undefined => {
  if (/^\d{3}\. .+/gu.test(title)) {
    return undefined;
  }

  return translate.t("validations.draftTitle");
};

const validFindingTypology: (titleSuggestions: string[]) => Validator =
  (titleSuggestions: string[]): Validator =>
  (title: string): string | undefined => {
    if (titleSuggestions.includes(title)) {
      return undefined;
    }

    return translate.t("validations.draftTypology");
  };

const isValidVulnSeverity: Validator = (value: string): string | undefined => {
  const min: number = 0;
  const max: number = 1000000000;
  if (
    _.isUndefined(
      isNumeric({ message: translate.t("validations.numeric") }, value)
    )
  ) {
    const severityBetween: (input: number) => string | undefined =
      numberBetween(min, max);

    return severityBetween(Number(value));
  }

  return translate.t("validations.between", { max, min });
};

const validDatetime: Validator = (value?: Dayjs | string): string | undefined =>
  isDayjs(value) ? undefined : translate.t("validations.datetime");

const validOptionalDatetime: Validator = (
  value?: Dayjs | string | undefined
): string | undefined =>
  _.isUndefined(value) || _.isEmpty(value) || isDayjs(value)
    ? undefined
    : translate.t("validations.datetime");

const isFloatOrInteger: Validator = (value: string): string | undefined => {
  function checkNumeric(valueToValidate: never): boolean {
    return !isNaN(valueToValidate - parseFloat(valueToValidate));
  }
  if (!checkNumeric(value as never)) {
    return translate.t("validations.numeric");
  }

  return undefined;
};

const isValidPhoneNumber: Validator = (
  value: IPhoneData | undefined
): string | undefined => {
  if (
    !_.isUndefined(value) &&
    /^(?:\d ?){6,11}\d$/u.test(value.nationalNumber)
  ) {
    return undefined;
  }

  return translate.t("validations.invalidPhoneNumber");
};

const getFileNameExtension: (filename: string) => string = (
  filename: string
): string => {
  const splittedName: string[] = filename.split(".");
  const extension: string =
    splittedName.length > 1 ? (_.last(splittedName) as string) : "";

  return extension.toLowerCase();
};

const getFileExtension: (file: File) => string = (file: File): string => {
  const splittedName: string[] = file.name.split(".");
  const extension: string =
    splittedName.length > 1 ? (_.last(splittedName) as string) : "";

  return extension.toLowerCase();
};

const hasExtension: (
  allowedExtensions: string[] | string,
  file?: File
) => boolean = (allowedExtensions: string[] | string, file?: File): boolean => {
  if (!_.isUndefined(file)) {
    return _.includes(allowedExtensions, getFileExtension(file));
  }

  return false;
};

const validEventFile: Validator = (value: FileList): string | undefined =>
  _.isEmpty(value) || hasExtension(["pdf", "zip", "csv", "txt"], _.first(value))
    ? undefined
    : translate.t("group.events.form.wrongFileType");

const validEvidenceImage: Validator = (
  value: FileList | undefined
): string | undefined =>
  _.isUndefined(value) ||
  (!_.isUndefined(value) &&
    [...Array(value.length).keys()].every((index: number): boolean =>
      hasExtension(["gif", "png", "webm"], value[index])
    ))
    ? undefined
    : translate.t("group.events.form.wrongImageType");

const isValidEvidenceName: (
  organizationName: string,
  groupName: string
) => Validator =
  (organizationName: string, groupName: string): Validator =>
  (file: FileList | undefined): string | undefined => {
    return _.isUndefined(file) ||
      (!_.isUndefined(file) &&
        [...Array(file.length).keys()].every((index: number): boolean => {
          const filename = file[index].name.toLocaleLowerCase();
          const extensions = getFileExtension(file[index]);
          const starts = `${organizationName.toLocaleLowerCase()}-${groupName.toLocaleLowerCase()}-`;
          const [ends] = filename.split(starts).slice(-1);
          const regex = /^[a-zA-Z0-9]{10}$/u;

          return (
            filename.startsWith(starts) &&
            regex.test(ends.replace(`.${extensions}`, ""))
          );
        }))
      ? undefined
      : translate.t("group.events.form.wrongImageName");
  };

const validExploitFile: Validator = (value: FileList): string | undefined =>
  hasExtension(["exp", "py"], _.first(value))
    ? undefined
    : translate.t("groupAlerts.fileTypePy");

const validRecordsFile: Validator = (value: FileList): string | undefined =>
  hasExtension("csv", _.first(value))
    ? undefined
    : translate.t("groupAlerts.fileTypeCsv");

const dateTimeBeforeToday: Validator = (date: Dayjs): string | undefined => {
  const today: Dayjs = dayjs();

  // Formik validation needs this seemingly unnecessary undefined check
  // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
  if (!(date instanceof dayjs)) {
    return undefined;
  }

  extend(isSameOrBefore);

  return date.isSameOrBefore(today)
    ? undefined
    : translate.t("validations.greaterDate");
};

const dateTimeBetween: (from: Dayjs, to: Dayjs) => Validator =
  (from: Dayjs, to: Dayjs): Validator =>
  (value?: Dayjs | string): string | undefined => {
    extend(isBetween);

    return isDayjs(value) && value.isBetween(from, to)
      ? undefined
      : translate.t("validations.datetimeBetween", {
          from: from.format("MM/DD/YYYY h:mm A"),
          to: to.format("MM/DD/YYYY h:mm A"),
        });
  };

const optionalDateTimeBetween: (from: Dayjs, to: Dayjs) => Validator =
  (from: Dayjs, to: Dayjs): Validator =>
  (value?: Dayjs | string | undefined): string | undefined => {
    extend(isBetween);

    return (isDayjs(value) && value.isBetween(from, to)) ||
      _.isUndefined(value) ||
      _.isEmpty(value)
      ? undefined
      : translate.t("validations.datetimeBetween", {
          from: from.format("MM/DD/YYYY h:mm A"),
          to: to.format("MM/DD/YYYY h:mm A"),
        });
  };

const isValidVulnsFile: Validator = (value: FileList): string | undefined => {
  if (_.isNil(value) || value.length === 0) {
    return translate.t("groupAlerts.noFileSelected");
  }
  // eslint-disable-next-line prefer-destructuring -- No destructuring as method returns an iterator
  const file: File = value[0];
  const MIB: number = 1048576;
  const fileType: string = `.${
    _.last(file.name.split(".")) as string
  }`.toLowerCase();
  if (file.size > Number(MIB)) {
    return translate.t("validations.fileSize", { count: 1 });
  } else if (!_.includes([".yml", ".yaml"], fileType)) {
    return translate.t("groupAlerts.fileTypeYaml");
  }

  return undefined;
};

const validTag: Validator = (value: string): string | undefined => {
  const pattern: RegExp = /^[a-z0-9]+(?:-[a-z0-9]+)*$/u;
  if (_.isEmpty(value) || !pattern.test(value)) {
    return translate.t("validations.tags");
  }

  return undefined;
};

const validField: Validator = (value: string): string | undefined => {
  const pattern: RegExp = /^(?!=).+/u;
  if (_.isEmpty(value) || !pattern.test(value)) {
    return translate.t("validations.invalidValueInField");
  }

  return undefined;
};

const validPath: (host: string | undefined) => Validator =
  (host: string | undefined): Validator =>
  (path: string): string | undefined => {
    const formmattedHost = host
      ?.replace("https://", "")
      .replace("http://", "")
      .slice(0, -1);
    if (
      (!_.isUndefined(formmattedHost) && path.includes(formmattedHost)) ||
      path.includes("https://") ||
      path.includes("http://")
    ) {
      return translate.t("validations.excludePathHost");
    }

    if (!_.isEmpty(path) && path.startsWith("/")) {
      return translate.t("validations.invalidTextBeginning", {
        chars: "/",
      });
    }

    return undefined;
  };

const isOptionalInteger = (value: unknown): string | undefined =>
  _.isInteger(value) || (_.isString(value) && _.isEmpty(value))
    ? undefined
    : translate.t("validations.integer");

const isValidEnvironmentUrl: (validEnvironmentUrls: string[]) => Validator =
  (validEnvironmentUrls: string[]): Validator =>
  (value: string): string | undefined =>
    validEnvironmentUrls.includes(value)
      ? undefined
      : translate.t("validations.invalidEnvironmentUrl");

const isValidFileName: Validator = (file: FileList): string | undefined => {
  const fileName: string = _.isEmpty(file) ? "" : file[0].name;
  const name: string[] = fileName.split(".");
  const validCharacters: RegExp = /^[A-Za-z0-9!\-_.*'()&$@=;:+,?\s]*$/u;

  return name.length <= 2 && validCharacters.test(fileName)
    ? undefined
    : translate.t("searchFindings.tabResources.invalidChars");
};

const isValidFileSize: (maxSize: number) => Validator =
  (maxSize: number): Validator =>
  (file: FileList | undefined): string | undefined => {
    const MIB: number = 1048576;

    return _.isUndefined(file) ||
      (!_.isUndefined(file) &&
        [...Array(file.length).keys()].every(
          (index: number): boolean => file[index].size < MIB * maxSize
        ))
      ? undefined
      : translate.t("validations.fileSize", { count: maxSize });
  };

const isValidAmountOfFiles: (maxFiles: number) => Validator =
  (maxFiles: number): Validator =>
  (file: FileList | undefined): string | undefined => {
    return _.isUndefined(file) ||
      (!_.isUndefined(file) && file.length <= maxFiles)
      ? undefined
      : translate.t("validations.amountOfFiles", { count: maxFiles });
  };

const isValidDateAccessToken: Validator = (
  value: string
): string | undefined => {
  const numberOfMonths: number = 6;
  const date: Date = new Date(value);
  const today: Date = new Date();

  const sixMonthsLater: Date = new Date(
    today.setMonth(today.getMonth() + numberOfMonths)
  );

  if (date > sixMonthsLater) {
    return translate.t("validations.validDateToken");
  }

  return undefined;
};

const isLowerDate: Validator = (value: string): string | undefined => {
  const date: Date = new Date(value);
  const today: Date = new Date();

  if (date <= today) {
    return translate.t("validations.lowerDate");
  }

  return undefined;
};

const isGreaterDate: Validator = (value: string): string | undefined => {
  const date: Date = new Date(value);
  const today: Date = new Date();

  if (date > today) {
    return translate.t("validations.greaterDate");
  }

  return undefined;
};

const excludeFormat: Validator = (
  value: string,
  allValues: Record<string, string>
): string | undefined => {
  const repoUrl: string = allValues.url;

  if (!_.isUndefined(repoUrl) && !_.isUndefined(value)) {
    const [urlBasename] = repoUrl.split("/").slice(-1);
    const repoName: string = urlBasename.endsWith(".git")
      ? urlBasename.replace(".git", "")
      : urlBasename;

    return value.toLowerCase().split("/").indexOf(repoName.toLowerCase()) === 0
      ? translate.t("validations.excludeFormat")
      : undefined;
  }

  return undefined;
};

const hasSshFormat: Validator = (value: string): string | undefined => {
  const regex =
    /^-{5}BEGIN OPENSSH PRIVATE KEY-{5}\n(?:[a-zA-Z0-9+/=]+\n)+-{5}END OPENSSH PRIVATE KEY-{5}\n?$/u;

  if (!regex.test(value)) {
    return translate.t("validations.invalidSshFormat");
  }

  return undefined;
};

const selected: Validator = (value: unknown): string | undefined =>
  value === true || value === false
    ? undefined
    : translate.t("validations.required");

export {
  regExps,
  composeValidators,
  required,
  someRequired,
  isValidEvidenceDescription,
  validTextField,
  validCsvInput,
  validUrlField,
  numberBetween,
  optionalDateTimeBetween,
  optionalNumberBetween,
  minLength,
  maxLength,
  sameValue,
  numeric,
  alphaNumeric,
  validAlphanumericSpace,
  validEmail,
  validDraftTitle,
  validPath,
  isOptionalInteger,
  isPositive,
  isZeroOrPositive,
  isValidAmountOfFiles,
  isValidEnvironmentUrl,
  isValidPhoneNumber,
  isValidVulnSeverity,
  isFloatOrInteger,
  validCommitHash,
  validDatetime,
  validEventFile,
  validEvidenceImage,
  validExploitFile,
  validFindingTypology,
  validRecordsFile,
  validOptionalDatetime,
  dateTimeBeforeToday,
  dateTimeBetween,
  getFileNameExtension,
  isValidVulnsFile,
  isValidEvidenceName,
  validTag,
  validField,
  isValidFileName,
  isValidFileSize,
  isValidDateAccessToken,
  isLowerDate,
  isGreaterDate,
  excludeFormat,
  hasSshFormat,
  selected,
};
