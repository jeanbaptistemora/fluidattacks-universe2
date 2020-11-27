import { Logger } from "utils/logger";
import type { Moment } from "moment";
import type { Validator } from "redux-form";
import _ from "lodash";
import moment from "moment";
import { translate } from "utils/translations/translate";
import {
  hasLengthGreaterThan,
  hasLengthLessThan,
  isAlphaNumeric,
  isNumeric,
  isRequired,
  matchesPattern,
} from "revalidate";

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
    const groupName: string = fieldId[0];

    return allValues[groupName];
  } else {
    Logger.error(
      `Fields must be grouped by a <FormSection> component`,
      new TypeError(
        `Field ${fieldId.toString()} must be grouped by a <FormSection> component`
      )
    );
  }
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

  return isValid ? undefined : translate.t("validations.some_required");
};

const validEvidenceDescription: Validator = (
  _0: boolean,
  allValues: Record<string, Record<string, unknown>>,
  _1: Record<string, unknown>,
  name: string
): string | undefined => {
  const groupValues: Record<string, unknown> | undefined = _.isEmpty(allValues)
    ? {}
    : getGroupValues(allValues, name);
  const hasDescription: boolean = _.has(groupValues, "description");
  const hasFileSelected: boolean = _.has(groupValues, "file");
  const hasUrl: boolean = _.has(groupValues, "url");

  return hasDescription
    ? hasUrl
      ? undefined
      : hasFileSelected
      ? undefined
      : translate.t("group_alerts.no_file_selected")
    : hasFileSelected
    ? translate.t("validations.required")
    : undefined;
};

const validTextField: Validator = (value: string): string | undefined => {
  if (!_.isNil(value)) {
    const beginTextMatch: RegExpMatchArray | null = /^=/u.exec(value);
    if (!_.isNull(beginTextMatch)) {
      return translate.t("validations.invalidTextBeginning", {
        chars: `'${beginTextMatch[0]}'`,
      });
    }

    // We use them for control character pattern matching.
    // eslint-disable-next-line no-control-regex
    const textMatch: RegExpMatchArray | null = /[^a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ \t\n\r\x0b\x0c(),./:;@_$#=?-]/u.exec(
      value
    );
    if (!_.isNull(textMatch)) {
      return translate.t("validations.invalidTextField", {
        chars: `'${textMatch[0]}'`,
      });
    }
  }
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

    const urlMatch: RegExpMatchArray | null = /[^a-zA-Z0-9(),./:;@_$#=?-]/u.exec(
      cleanValue
    );
    if (!_.isNull(urlMatch)) {
      return translate.t("validations.invalidUrlField", {
        chars: `'${urlMatch[0]}'`,
      });
    }
  }
};

const numberBetween: (min: number, max: number) => Validator = (
  min: number,
  max: number
): Validator => (value: number): string | undefined =>
  value < min || value > max
    ? translate.t("validations.between", { max, min })
    : undefined;

const minLength: (min: number) => Validator = (min: number): Validator =>
  hasLengthGreaterThan(min - 1)({
    message: translate.t("validations.minLength", { count: min }),
  }) as Validator;

const maxLength: (max: number) => Validator = (max: number): Validator =>
  hasLengthLessThan(max)({
    message: translate.t("validations.maxLength", { count: max }),
  }) as Validator;

const sameValue: (projectName: string) => Validator = (
  projectName: string
): Validator => (value: string): string | undefined =>
  value !== projectName ? translate.t("validations.required") : undefined;

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

const validDraftTitle: (title: string) => string | undefined = (
  title: string
): string | undefined => {
  if (/^[A-Z]+\.(H\.|S\.|SH\.)??[0-9]+\. .+/gu.test(title)) {
    return undefined;
  }

  return translate.t("validations.draftTitle");
};

const isValidVulnSeverity: Validator = (value: string): string | undefined => {
  const min: number = 0;
  const max: number = 1000000000;
  if (
    _.isUndefined(
      isNumeric({ message: translate.t("validations.numeric") }, value)
    )
  ) {
    const severityBetween: (
      input: number
    ) => string | undefined = numberBetween(min, max);

    return severityBetween(Number(value));
  }

  return translate.t("validations.between", { max, min });
};

const validDatetime: Validator = (
  value?: Moment | string
): string | undefined =>
  moment.isMoment(value) ? undefined : translate.t("validations.datetime");

const getFileExtension: (file: File) => string = (file: File): string => {
  const splittedName: string[] = file.name.split(".");
  const extension: string =
    splittedName.length > 1 ? (_.last(splittedName) as string) : "";

  return extension.toLowerCase();
};

const hasExtension: (
  allowedExtensions: string | string[],
  file?: File
) => boolean = (allowedExtensions: string | string[], file?: File): boolean => {
  if (!_.isUndefined(file)) {
    return _.includes(allowedExtensions, getFileExtension(file));
  }

  return false;
};

const validEventFile: Validator = (value: FileList): string | undefined =>
  _.isEmpty(value) || hasExtension(["pdf", "zip", "csv", "txt"], _.first(value))
    ? undefined
    : translate.t("group.events.form.wrong_file_type");

const validEvidenceImage: Validator = (value: FileList): string | undefined =>
  _.isEmpty(value) || hasExtension(["gif", "png"], _.first(value))
    ? undefined
    : translate.t("group.events.form.wrong_image_type");

const validExploitFile: Validator = (value: FileList): string | undefined =>
  hasExtension(["exp", "py"], _.first(value))
    ? undefined
    : translate.t("group_alerts.file_type_py");

const validRecordsFile: Validator = (value: FileList): string | undefined =>
  hasExtension("csv", _.first(value))
    ? undefined
    : translate.t("group_alerts.file_type_csv");

const dateTimeBeforeToday: Validator = (date: Moment): string | undefined => {
  const today: Moment = moment();

  return date.isSameOrBefore(today)
    ? undefined
    : translate.t("validations.greater_date");
};

const isValidVulnsFile: Validator = (value: FileList): string | undefined => {
  if (_.isNil(value) || value.length === 0) {
    return translate.t("group_alerts.no_file_selected");
  } else {
    const file: File = value[0];
    const MIB: number = 1048576;
    const fileType: string = `.${
      _.last(file.name.split(".")) as string
    }`.toLowerCase();
    if (file.size > MIB * 1) {
      return translate.t("validations.file_size", { count: 1 });
    } else if (!_.includes([".yml", ".yaml"], fileType)) {
      return translate.t("group_alerts.file_type_yaml");
    } else {
      return undefined;
    }
  }
};

const validTag: Validator = (value: string): string | undefined => {
  const pattern: RegExp = /^[a-z0-9]+(?:-[a-z0-9]+)*$/u;
  if (_.isEmpty(value) || !pattern.test(value)) {
    return translate.t("validations.tags");
  } else {
    return undefined;
  }
};

const validField: Validator = (value: string): string | undefined => {
  const pattern: RegExp = /^(?!=).+/u;
  if (_.isEmpty(value) || !pattern.test(value)) {
    return translate.t("validations.invalidValueInField");
  } else {
    return undefined;
  }
};

const isValidFileName: Validator = (file: FileList): string | undefined => {
  const fileName: string = _.isEmpty(file) ? "" : file[0].name;
  const name: string[] = fileName.split(".");
  const validCharacters: RegExp = /^[A-Za-z0-9!\-_.*'()&$@=;:+,?\s]*$/u;

  return name.length <= 2 && validCharacters.test(fileName)
    ? undefined
    : translate.t("search_findings.tab_resources.invalid_chars");
};

const isValidFileSize: (maxSize: number) => Validator = (
  maxSize: number
): Validator => (file: FileList): string | undefined => {
  const MIB: number = 1048576;

  return _.isEmpty(file) || file[0].size < MIB * maxSize
    ? undefined
    : translate.t("validations.file_size", { count: maxSize });
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
    return translate.t("validations.valid_date_token");
  }
};

const isLowerDate: Validator = (value: string): string | undefined => {
  const date: Date = new Date(value);
  const today: Date = new Date();

  if (date <= today) {
    return translate.t("validations.lower_date");
  }
};

export {
  required,
  someRequired,
  validEvidenceDescription,
  validTextField,
  validUrlField,
  numberBetween,
  minLength,
  maxLength,
  sameValue,
  numeric,
  alphaNumeric,
  validAlphanumericSpace,
  validEmail,
  validDraftTitle,
  isValidVulnSeverity,
  validDatetime,
  validEventFile,
  validEvidenceImage,
  validExploitFile,
  validRecordsFile,
  dateTimeBeforeToday,
  isValidVulnsFile,
  validTag,
  validField,
  isValidFileName,
  isValidFileSize,
  isValidDateAccessToken,
  isLowerDate,
};
