import _ from "lodash";
import { IFormData, IGroupData } from "scenes/Dashboard/containers/ProjectSettingsView/Services/types";
import { translate } from "utils/translations/translate";

const serviceStateToString: ((value: boolean | string | undefined) => string) =
  (value: boolean | string | undefined): string => {
    let service: string;

    switch (typeof(value)) {
      case "boolean":
        service = value ? "active" : "inactive";
        break;
      case "string":
        service =
          value
            .toLowerCase()
            .replace("_", "");
        break;
      default:
        service = "";
    }

    return service;
  };

const serviceDiff: ((msg: string, old: string, now: string) => string) =
  (msg: string, old: string, now: string): string => {
    const as: string = translate.t("search_findings.services_table.modal.diff.as");
    const from: string = translate.t("search_findings.services_table.modal.diff.from");
    const keep: string = translate.t("search_findings.services_table.modal.diff.keep");
    const mod: string = translate.t("search_findings.services_table.modal.diff.mod");
    const to: string = translate.t("search_findings.services_table.modal.diff.to");

    const msgString: string = translate.t(`search_findings.services_table.${msg}`);
    const nowString: string = translate.t(`search_findings.services_table.${now}`);
    const oldString: string = translate.t(`search_findings.services_table.${old}`);

    return now === old
      ? `${keep} ${msgString} ${as} ${nowString}`
      : `${mod} ${msgString} ${from} ${oldString} ${to} ${nowString} *`;
  };

export const computeConfirmationMessage: ((data: IGroupData, form: IFormData) => string[]) =
  (data: IGroupData, form: IFormData): string[] => ([
      serviceDiff("type", serviceStateToString(data.project.subscription), serviceStateToString(form.type)),
      serviceDiff("group", serviceStateToString(true), serviceStateToString(form.integrates ? true : "deleted_soon")),
      serviceDiff("integrates", serviceStateToString(true), serviceStateToString(form.integrates)),
      serviceDiff("drills", serviceStateToString(data.project.hasDrills), serviceStateToString(form.drills)),
      serviceDiff("forces", serviceStateToString(data.project.hasForces), serviceStateToString(form.forces)),
    ]
  );

export const isDowngrading: ((before: boolean | undefined, after: boolean | undefined) => boolean) =
  (before: boolean | undefined, after: boolean | undefined): boolean =>
    before === true && after === false;

export const isDowngradingServices: ((data: IGroupData, form: IFormData) => boolean) =
  (data: IGroupData, form: IFormData): boolean => ([
    isDowngrading(true, form.integrates),
    isDowngrading(data.project.hasDrills, form.drills),
    isDowngrading(data.project.hasForces, form.forces),
  ].some((result: boolean) => result));
