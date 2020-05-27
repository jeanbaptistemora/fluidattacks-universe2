import translate from "../../../../../utils/translations/translate";
import { IFormData, IGroupData } from "./types";

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
      : `${mod} ${msgString} ${from} ${oldString} ${to} ${nowString}`;
  };

export const computeConfirmationMessage: ((data: IGroupData, form: IFormData) => string) =
  (data: IGroupData, form: IFormData): string => ([
      serviceDiff("type", serviceStateToString(data.project.subscription), serviceStateToString(form.type)),
      serviceDiff("integrates", serviceStateToString(true), serviceStateToString(form.integrates)),
      serviceDiff("drills", serviceStateToString(data.project.hasDrills), serviceStateToString(form.drills)),
      serviceDiff("forces", serviceStateToString(data.project.hasForces), serviceStateToString(form.forces)),
    ].filter((line: string): boolean => line.length > 0)
      .join("\n")
  );
