import _ from "lodash";
import { isRequired } from "revalidate";
import { msgError } from "./notifications";
import translate from "./translations/translate";

export const required: typeof isRequired = isRequired({
  message: "This field is required.",
});

export const validEmail: ((arg1: string) => string | undefined) =
  (value: string): string | undefined => {
  const pattern: RegExp = /^[a-zA-Z0-9.!#$%&’*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/i;
  if (_.isEmpty(value) || !pattern.test(value)) {
    return "The email format is not valid.";
  } else {
    return undefined;
  }
};

const evidenceHasValidType: ((arg1: File, arg2: number) => boolean) =
  (file: File, evidenceType: number): boolean => {
  let valid: boolean;
  let ANIMATION: number; ANIMATION = 0;
  let EVIDENCE: number[]; EVIDENCE = [1, 2, 3, 4, 5, 6];
  let EXPLOIT: number; EXPLOIT = 7;
  let RECORDS: number; RECORDS = 8;
  const fileType: string = `.${_.last(file.name.split("."))}`.toLowerCase();

  if (evidenceType === ANIMATION) {
    valid = fileType === ".gif";
    if (!valid) {
      msgError(translate.t("proj_alerts.file_type_gif"));
    }
  } else if (_.includes(EVIDENCE, evidenceType)) {
    valid = fileType === ".png";
    if (!valid) {
      msgError(translate.t("proj_alerts.file_type_png"));
    }
  } else if (evidenceType === EXPLOIT) {
    valid = fileType === ".py";
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

const evidenceHasValidSize: ((arg1: File) => boolean) = (file: File): boolean => {
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
      valid = file.size < MIB * 1;
      if (!valid) {
        msgError(translate.t("proj_alerts.file_size_py"));
      }
      break;
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
