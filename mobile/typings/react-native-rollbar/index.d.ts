// Patch missing react-native-rollbar typings.
declare module "rollbar/src/react-native/rollbar" {
  export = Rollbar;

  declare class Rollbar {
    constructor(options?: Rollbar.Configuration);
    static init(options: Rollbar.Configuration): Rollbar;

    public global(options: Rollbar.Configuration): Rollbar;
    public configure(options: Rollbar.Configuration): Rollbar;
    public lastError(): Rollbar.MaybeError;

    public log(...args: Rollbar.LogArgument[]): Rollbar.LogResult;
    public debug(...args: Rollbar.LogArgument[]): Rollbar.LogResult;
    public info(...args: Rollbar.LogArgument[]): Rollbar.LogResult;
    public warn(...args: Rollbar.LogArgument[]): Rollbar.LogResult;
    public warning(...args: Rollbar.LogArgument[]): Rollbar.LogResult;
    public error(...args: Rollbar.LogArgument[]): Rollbar.LogResult;
    public critical(...args: Rollbar.LogArgument[]): Rollbar.LogResult;
    public wait(callback: () => void): void;

    public captureEvent(metadata: object, level: Rollbar.Level): Rollbar.TelemetryEvent;
  }

  declare namespace Rollbar {
    export type MaybeError = Error | undefined | null;
    export type Level = "debug" | "info" | "warning" | "error" | "critical";
    export interface Configuration {
      accessToken?: string;
      version?: string;
      environment?: string;
      logLevel?: Level;
      reportLevel?: Level;
      uncaughtErrorLevel?: Level;
      verbose?: boolean;
      enabled?: boolean;
      captureUncaught?: boolean;
      captureUnhandledRejections?: boolean;
    }
    export type Callback = (err: MaybeError, response: object) => void;
    export type LogArgument = string | Error | object | Callback | Date | any[];
    export interface LogResult {
      uuid: string;
    }
    export interface TelemetryEvent {
      level: Level;
      type: string;
      timestamp_ms: number;
      body: object;
      source: string;
      uuid?: string;
    }
  }
}
