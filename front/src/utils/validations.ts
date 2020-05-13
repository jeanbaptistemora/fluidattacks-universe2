import _ from "lodash";
import moment, { Moment } from "moment";
import { Validator } from "redux-form";
import {
  hasLengthGreaterThan, hasLengthLessThan, isAlphaNumeric, isNumeric, isRequired, matchesPattern,
} from "revalidate";
import { msgError } from "./notifications";
import translate from "./translations/translate";

export const required: Validator = isRequired({
  message: translate.t("validations.required"),
});

const getGroupValues: ((allValues: Dictionary, name: string) => Dictionary) = (
  allValues: Dictionary, name: string,
): Dictionary => {
  const fieldId: string[] = name.split(".");

  if (fieldId.length > 1) {
    const groupName: string = fieldId[0];

    return allValues[groupName];
  } else {
    throw new TypeError(`Field ${fieldId} must be grouped by a <FormSection> component`);
  }
};

export const someRequired: Validator = (
  _0: boolean, allValues: { [key: string]: {} }, _1: {}, name: string,
): string | undefined => {
  const groupValues: Dictionary = getGroupValues(allValues, name);
  const isValid: boolean = _.some(groupValues);

  return isValid ? undefined : translate.t("validations.some_required");
};

export const validEvidenceDescription: Validator = (
  _0: boolean, allValues: { [key: string]: {} }, _1: {}, name: string,
): string | undefined => {

  const groupValues: Dictionary = _.isEmpty(allValues) ? {} : getGroupValues(allValues, name);
  const hasDescription: boolean = !_.isEmpty(groupValues.description);
  const hasFileSelected: boolean = !_.isEmpty(groupValues.file as FileList);
  const hasUrl: boolean = !_.isEmpty(groupValues.url);

  return hasDescription
    ? hasUrl
      ? undefined
      : hasFileSelected
        ? undefined
        : translate.t("proj_alerts.no_file_selected")
    : hasFileSelected
      ? translate.t("validations.required")
      : undefined;
};

export const validTextField: Validator = (value: string): string | undefined => {
  const riskStartChars: string[] = ["=", "?", "<", "`"];
  const riskChars: string[] = ["'", "`"];
  let ret: string | undefined;
  if (!_.isNil(value) && riskChars.some((char: string) => value.includes(char))) {
    ret = translate.t("validations.invalidTextField", { chars: riskChars });
  } else if (!_.isNil(value) && riskStartChars.includes(value[0])) {
    ret = translate.t("validations.invalidTextFieldStart", { chars: riskStartChars });
  }

  return ret;
};

export const numberBetween: ((min: number, max: number) => Validator) =
  (min: number, max: number): Validator =>
    (value: number): string | undefined =>
      value < min || value > max ? translate.t("validations.between", { min, max }) : undefined;

export const minLength: ((min: number) => Validator) = (min: number): Validator =>
  hasLengthGreaterThan(min - 1)({ message: translate.t("validations.minLength", { count: min }) });

export const maxLength: ((max: number) => Validator) = (max: number): Validator =>
  hasLengthLessThan(max)({ message: translate.t("validations.maxLength", { count: max }) });

export const sameValue: ((projectName: string) => Validator) = (projectName: string): Validator =>
  (value: string): string | undefined => value !== projectName ? translate.t("validations.required") : undefined;

export const numeric: Validator = isNumeric({
  message: translate.t("validations.numeric"),
});

export const alphaNumeric: Validator = isAlphaNumeric({
  message: translate.t("validations.alphanumeric"),
});

export const validAlphanumericSpace: Validator = matchesPattern(
  /^[a-z\d\s]+$/i,
)({
  message: translate.t("validations.alphanumeric"),
});

export const validEmail: Validator = matchesPattern(
  /^[a-zA-Z0-9.!#$%&’*/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,
)({
  message: translate.t("validations.email"),
});

export const validDraftTitle: ((title: string) => string | undefined) = (title: string): string | undefined => {
  if (/^[A-Z]+\.(H\.|S\.|SH\.)??[0-9]+\. .+/g.test(title)) {

    return undefined;
  }

  return translate.t("validations.draftTitle");
};

export const isValidVulnSeverity: Validator = (value: string): string | undefined => {
  const min: number = 0;
  const max: number = 1000000000;
  if (_.isUndefined(isNumeric({ message: translate.t("validations.numeric") }, value))) {
    const severityBetween: ((value: number) => string | undefined) = numberBetween(min, max);

    return severityBetween(Number(value));
  }

  return translate.t("validations.between", { min, max });
};

export const validDatetime: Validator = (value?: Moment | string): string | undefined => (
  moment.isMoment(value) ? undefined : translate.t("validations.datetime")
);

const getFileExtension: ((file: File) => string) = (file: File): string => {
  const splittedName: string[] = file.name.split(".");
  const extension: string = splittedName.length > 1 ? _.last(splittedName) as string : "";

  return extension.toLowerCase();
};

const hasExtension: ((allowedExtensions: string | string[], file?: File) => boolean) = (
  allowedExtensions: string | string[], file?: File,
): boolean => {
  let isValid: boolean = false;

  if (file !== undefined) {
    isValid = _.includes(allowedExtensions, getFileExtension(file));
  }

  return isValid;
};

export const validEventFile: Validator = (value: FileList): string | undefined => (
  _.isEmpty(value) || hasExtension(["pdf", "zip", "csv", "txt"], _.first(value))
    ? undefined
    : translate.t("project.events.form.wrong_file_type")
);

export const validEvidenceImage: Validator = (value: FileList): string | undefined => (
  _.isEmpty(value) || hasExtension(["gif", "jpg", "jpeg", "png"], _.first(value))
    ? undefined
    : translate.t("project.events.form.wrong_image_type")
);

export const validExploitFile: Validator = (value: FileList): string | undefined => (
  hasExtension(["exp", "py"], _.first(value))
    ? undefined
    : translate.t("proj_alerts.file_type_py")
);

export const validRecordsFile: Validator = (value: FileList): string | undefined => (
  hasExtension("csv", _.first(value))
    ? undefined
    : translate.t("proj_alerts.file_type_csv")
);

export const dateTimeBeforeToday: Validator = (date: Moment): string | undefined => {
  const today: Moment = moment();

  return date.isSameOrBefore(today) ? undefined : translate.t("validations.greater_date");
};

export const isValidVulnsFile: ((fieldId: string) => boolean) = (fieldId: string): boolean => {
  const selected: FileList | null = (document.querySelector(fieldId) as HTMLInputElement).files;
  let valid: boolean; valid = false;

  if (_.isNil(selected) || selected.length === 0) {
    msgError(translate.t("proj_alerts.no_file_selected"));
  } else {
    const file: File = selected[0];
    let MIB: number; MIB = 1048576;
    const fileType: string = `.${_.last(file.name.split("."))}`.toLowerCase();

    if (file.size > MIB * 1) {
      msgError(translate.t("validations.file_size", { count: 1 }));
    } else if (!_.includes([".yml", ".yaml"], fileType)) {
      msgError(translate.t("proj_alerts.file_type_yaml"));
    } else {
      valid = true;
    }
  }

  return valid;
};

export const validTag: Validator = (value: string): string | undefined => {
  const pattern: RegExp = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
  if (_.isEmpty(value) || !pattern.test(value)) {
    return translate.t("validations.tags");
  } else {
    return undefined;
  }
};

export const validField: Validator = (value: string): string | undefined => {
  const pattern: RegExp = /^(?!=).+/;
  if (_.isEmpty(value) || !pattern.test(value)) {
    return translate.t("validations.invalidValueInField");
  } else {
    return undefined;
  }
};

export const isValidFileName: Validator = (file: FileList): string | undefined => {
  const fileName: string = _.isEmpty(file) ? "" : file[0].name;
  const name: string[] = fileName.split(".");
  const validCharacters: RegExp = /^[A-Za-z0-9!\-_.*'()&$@=;:+,?\s]*$/;

  return name.length <= 2 && validCharacters.test(fileName)
    ? undefined
    : translate.t("search_findings.tab_resources.invalid_chars");
};

export const isValidFileSize: ((maxSize: number) => Validator) = (maxSize: number): Validator =>
  (file: FileList): string | undefined => {
    const MIB: number = 1048576;

    return _.isEmpty(file) || file[0].size < MIB * maxSize
      ? undefined
      : translate.t("validations.file_size", { count: maxSize });
  };

export const isValidDate: ((arg1: string) => string | undefined) = (value: string): string | undefined => {
  let date: Date; date = new Date(value);
  let today: Date; today = new Date(); today = new Date(today.setMonth(today.getMonth() + 6));

  if (date > today) {
    return translate.t("validations.valid_date");
  } else {
    return undefined;
  }
};

export const isValidDateAccessToken: Validator = (value: string): string | undefined => {
  let date: Date; date = new Date(value);
  let today: Date; today = new Date(); today = new Date(today.setMonth(today.getMonth() + 6));

  if (date > today) {
    return translate.t("validations.valid_date_token");
  } else {
    return undefined;
  }
};

export const isLowerDate: Validator = (value: string): string | undefined => {
  let date: Date; date = new Date(value);
  let today: Date; today = new Date();

  if (date <= today) {
    return translate.t("validations.lower_date");
  } else {
    return undefined;
  }
};
