import _ from "lodash";
import { ConfigurableValidator, ConfiguredValidator, hasLengthGreaterThan, isAlphaNumeric, isNumeric,
  isRequired } from "revalidate";
import { msgError } from "./notifications";
import translate from "./translations/translate";

export const required: ConfiguredValidator = isRequired({
  message: translate.t("validations.required"),
});

export const numberBetween: ((min: number, max: number) => ((value: number) => string | undefined)) =
  (min: number, max: number): ((value: number) => string | undefined) =>
    (value: number): string | undefined =>
      value < min || value > max ? translate.t("validations.between", { min, max }) : undefined;

export const minLength: ((min: number) => ConfigurableValidator) = (min: number): ConfigurableValidator =>
  hasLengthGreaterThan(min - 1)({ message: translate.t("validations.minLength", { count: min }) });

export const numeric: ConfiguredValidator = isNumeric({
  message: translate.t("validations.numeric"),
});

export const alphaNumeric: ConfiguredValidator = isAlphaNumeric({
  message: translate.t("validations.alphanumeric"),
});

export const validEmail: ((arg1: string) => string | undefined) =
  (value: string): string | undefined => {
  const pattern: RegExp = /^[a-zA-Z0-9.!#$%&’*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/i;
  if (_.isEmpty(value) || !pattern.test(value)) {
    return translate.t("validations.email");
  } else {
    return undefined;
  }
};

export const evidenceHasValidType: ((arg1: File, arg2: number) => boolean) =
  (file: File, evidenceType: number): boolean => {
  let valid: boolean;
  let ANIMATION: number; ANIMATION = 0;
  let EVIDENCE: number[]; EVIDENCE = [1, 2, 3, 4, 5, 6];
  let EXPLOIT: number; EXPLOIT = 7;
  let RECORDS: number; RECORDS = 8;
  const fileType: string = `.${_.last(file.name.split("."))}`.toLowerCase();

  if (evidenceType === ANIMATION || (_.includes(EVIDENCE, evidenceType))) {
    valid = fileType === ".gif" || fileType === ".png";
    if (!valid) {
      msgError(translate.t("proj_alerts.file_type_evidence"));
    }
  } else if (evidenceType === EXPLOIT) {
    valid = fileType === ".py" || fileType === ".exp";
    if (!valid) {
      msgError(translate.t("proj_alerts.file_type_py"));
    }
  } else if (evidenceType === RECORDS) {
    valid = fileType === ".csv";
    if (!valid) {
      msgError(translate.t("proj_alerts.file_type_csv"));
    }
  } else {
    valid = false;
    msgError(translate.t("proj_alerts.file_type_wrong"));
  }

  return valid;
};

export const evidenceHasValidSize: ((arg1: File) => boolean) = (file: File): boolean => {
  let valid: boolean;
  let MIB: number; MIB = 1048576;
  const fileType: string = `.${_.last(file.name.split("."))}`.toLowerCase();

  switch (fileType) {
    case ".gif":
      valid = file.size < MIB * 10;
      if (!valid) {
        msgError(translate.t("proj_alerts.file_size"));
      }
      break;
    case ".png":
      valid = file.size < MIB * 2;
      if (!valid) {
        msgError(translate.t("proj_alerts.file_size_png"));
      }
      break;
    case ".py":
    case ".exp":
    case ".csv":
      valid = file.size < MIB * 1;
      if (!valid) {
        msgError(translate.t("proj_alerts.file_size_py"));
      }
      break;
    default:
      valid = false;
      msgError(translate.t("proj_alerts.file_type_wrong"));
  }

  return valid;
};

export const isValidEvidenceFile: ((arg1: string) => boolean) =
  (fieldId: string): boolean => {
    const selected: FileList | null = (document.querySelector(fieldId) as HTMLInputElement).files;
    let valid: boolean; valid = false;

    if (_.isNil(selected) || selected.length === 0) {
      msgError(translate.t("proj_alerts.no_file_selected"));
    } else {
      const evidenceType: number = Number(fieldId.charAt(fieldId.length - 1));
      valid = evidenceHasValidType(selected[0], evidenceType) && evidenceHasValidSize(selected[0]);
    }

    return valid;
};

export const isFileSelected: ((arg1: string) => boolean) =
  (fieldId: string): boolean => {
    const selected: FileList | null = (document.querySelector(fieldId) as HTMLInputElement).files;

    return !(_.isNil(selected) || selected.length === 0);
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
      msgError(translate.t("proj_alerts.file_size_py"));
    } else if (!_.includes([".yml", ".yaml"], fileType)) {
      msgError(translate.t("proj_alerts.file_type_yaml"));
    } else {
      valid = true;
    }
  }

  return valid;
};

export const validTag: ((arg1: string) => string | undefined) =
  (value: string): string | undefined => {
  const pattern: RegExp = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
  if (_.isEmpty(value) || !pattern.test(value)) {
    return translate.t("validations.tags");
  } else {
    return undefined;
  }
};

export const isValidFileName: ((arg1: string) => boolean) =
  (fileName: string): boolean => {
    let valid: boolean; valid = false;
    let name: string[]; name = fileName.split(".");
    const validCharacters: RegExp = /^[A-Za-z0-9!\-_.*'()&$@=;:+,?\s]*$/;

    if (name.length <= 2) {
      valid = validCharacters.test(fileName);
    }

    return valid;
};

export const isValidFileSize: ((file: File, fileSize: number) => boolean) =
  (file: File, fileSize: number): boolean => {

  let MIB: number; MIB = 1048576;
  let isValid: boolean; isValid = false;
  if (file.size > MIB * fileSize) {
    msgError(translate.t("validations.file_size", { count: fileSize }));
  } else {
    isValid = true;
  }

  return isValid;
};

export const isValidDate: ((arg1: string) => string | undefined) =
  (value: string): string | undefined => {
  let date: Date; date = new Date(value);
  let today: Date; today = new Date(); today = new Date(today.setMonth(today.getMonth() + 6));

  if (date > today) {
    return translate.t("validations.valid_date");
  } else {
    return undefined;
  }
};

export const isValidDateAccessToken: ((arg1: string) => string | undefined) =
  (value: string): string | undefined => {
  let date: Date; date = new Date(value);
  let today: Date; today = new Date(); today = new Date(today.setMonth(today.getMonth() + 6));

  if (date > today) {
    return translate.t("validations.valid_date_token");
  } else {
    return undefined;
  }
};

export const isLowerDate: ((arg1: string) => string | undefined) =
  (value: string): string | undefined => {
  let date: Date; date = new Date(value);
  let today: Date; today = new Date();

  if (date <= today) {
    return translate.t("validations.lower_date");
  } else {
    return undefined;
  }
};
