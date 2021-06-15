import type {
  IFormData,
  IGroupData,
} from "scenes/Dashboard/containers/GroupSettingsView/Services/types";
import { translate } from "utils/translations/translate";

const serviceStateToString: (value: boolean | string | undefined) => string = (
  value: boolean | string | undefined
): string => {
  switch (typeof value) {
    case "boolean":
      return value ? "active" : "inactive";
    case "string":
      return value.toLowerCase().replace("_", "");
    default:
      return "";
  }
};

const serviceDiff: (msg: string, old: string, now: string) => string = (
  msg: string,
  old: string,
  now: string
): string => {
  const as: string = translate.t("searchFindings.servicesTable.modal.diff.as");
  const from: string = translate.t(
    "searchFindings.servicesTable.modal.diff.from"
  );
  const keep: string = translate.t(
    "searchFindings.servicesTable.modal.diff.keep"
  );
  const mod: string = translate.t(
    "searchFindings.servicesTable.modal.diff.mod"
  );
  const to: string = translate.t("searchFindings.servicesTable.modal.diff.to");

  const msgString: string = translate.t(`searchFindings.servicesTable.${msg}`);
  const nowString: string = translate.t(`searchFindings.servicesTable.${now}`);
  const oldString: string = translate.t(`searchFindings.servicesTable.${old}`);

  return now === old
    ? `${keep} ${msgString} ${as} ${nowString}`
    : `${mod} ${msgString} ${from} ${oldString} ${to} ${nowString} *`;
};

const computeConfirmationMessage: (
  data: IGroupData,
  form: IFormData
) => string[] = (data: IGroupData, form: IFormData): string[] => [
  serviceDiff(
    "type",
    serviceStateToString(data.group.subscription),
    serviceStateToString(form.type)
  ),
  serviceDiff(
    "group",
    serviceStateToString(true),
    serviceStateToString(form.asm ? true : "deleted_soon")
  ),
  serviceDiff(
    "asm",
    serviceStateToString(true),
    serviceStateToString(form.asm)
  ),
  serviceDiff(
    "machine",
    serviceStateToString(data.group.hasSkims),
    serviceStateToString(form.machine)
  ),
  serviceDiff(
    "squad",
    serviceStateToString(data.group.hasDrills),
    serviceStateToString(form.squad)
  ),
  serviceDiff(
    "forces",
    serviceStateToString(data.group.hasForces),
    serviceStateToString(form.forces)
  ),
];

const isDowngrading: (
  before: boolean | undefined,
  after: boolean | undefined
) => boolean = (
  before: boolean | undefined,
  after: boolean | undefined
): boolean => before === true && after === false;

const isDowngradingServices: (data: IGroupData, form: IFormData) => boolean = (
  data: IGroupData,
  form: IFormData
): boolean =>
  [
    isDowngrading(true, form.asm),
    isDowngrading(data.group.hasSkims, form.machine),
    isDowngrading(data.group.hasDrills, form.squad),
    isDowngrading(data.group.hasForces, form.forces),
  ].some((result: boolean): boolean => result);

export { computeConfirmationMessage, isDowngrading, isDowngradingServices };
