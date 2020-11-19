import Bugsnag from "@bugsnag/js";
import type { Error } from "@bugsnag/core/types/event";
import type Event from "@bugsnag/core/types/event";

interface ILoggerAttr {
  error: (msg: string, extra?: unknown) => void;
  warning: (msg: string, extra?: unknown) => void;
}

const sendBugsnagReport: (
  msg: string,
  extra: unknown,
  severity: "info" | "warning" | "error"
) => void = (
  msg: string,
  extra: unknown,
  severity: "info" | "warning" | "error"
): void => {
  Bugsnag.notify(msg, (event: Event): void => {
    event.errors.forEach((error: Error): void => {
      // eslint-disable-next-line fp/no-mutation
      error.errorClass = `Log${severity.toUpperCase()}`;

      // eslint-disable-next-line fp/no-mutating-methods
      error.stacktrace.splice(0, 2);
    });
    event.addMetadata("extra", { extra: extra });

    // eslint-disable-next-line fp/no-mutation
    event.severity = severity;
  });
};

const sendErrorReport: (msg: string, extra?: unknown) => void = (
  msg: string,
  extra: unknown = {}
): void => {
  sendBugsnagReport(msg, extra, "error");
};

const sendWarningReport: (msg: string, extra?: unknown) => void = (
  msg: string,
  extra: unknown = {}
): void => {
  sendBugsnagReport(msg, extra, "warning");
};

export const Logger: ILoggerAttr = {
  error: sendErrorReport,
  warning: sendWarningReport,
};
