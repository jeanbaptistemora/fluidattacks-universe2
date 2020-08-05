// It is necessary to import the event types
// tslint:disable-next-line:no-submodule-imports
import Event, { Error } from "@bugsnag/core/types/event";
import Bugsnag from "@bugsnag/expo";

/**
 * Logger attributes
 */
interface ILoggerAttr {
  error(msg: string, extra?: unknown): void;
  warning(msg: string, extra?: unknown): void;
}

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

export const LOGGER: ILoggerAttr = {
  error: sendErrorReport,
  warning: sendWarningReport,
};
