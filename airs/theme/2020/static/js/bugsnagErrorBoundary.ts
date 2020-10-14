import { Event } from "@bugsnag/core";
// tslint:disable-next-line:no-submodule-imports
import { Error } from "@bugsnag/core/types/event";
import Bugsnag from "@bugsnag/js";
import _ from "lodash";

import { getEnvironment } from "./getEnvironment";

const { userEmail, userName } = window as typeof window & IDictionary<string>;

export const startBugsnag: (() => void) = (): void => {
  Bugsnag.start({
    apiKey: "6d0d7e66955855de59cfff659e6edf31",
    appVersion: "airs_version",
    releaseStage: getEnvironment(),
    user: {
      email: userEmail,
      name: userName,
    },
  });
};

const sendBugsnagReport: (
  msg: string,
  extra: unknown,
  severity: "info" | "warning" | "error",
) => void = (
  msg: string,
  extra: unknown,
  severity: "info" | "warning" | "error",
): void => {
  Bugsnag.notify(msg, (event: Event): void => {
    event.errors.forEach((error: Error): void => {
      error.errorClass = `Log${severity.toUpperCase()}`;

      error.stacktrace.splice(0, 2);
    });
    event.addMetadata("extra", { extra });

    event.severity = severity;
  });
};

const sendErrorReport: (msg: string, extra?: unknown) => void = (
  msg: string,
  extra: unknown = {},
): void => {
  sendBugsnagReport(msg, extra, "error");
};

const sendWarningReport: (msg: string, extra?: unknown) => void = (
  msg: string,
  extra: unknown = {},
): void => {
  sendBugsnagReport(msg, extra, "warning");
};

export const logger: ILoggerAttr = {
  error: sendErrorReport,
  warning: sendWarningReport,
};
