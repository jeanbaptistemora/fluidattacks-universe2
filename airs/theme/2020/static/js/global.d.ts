interface IDictionary<T = {}> { [key: string]: T; }

interface ILoggerAttr {
  // tslint:disable-next-line: completed-docs
  error(msg: string, extra?: unknown): void;
  // tslint:disable-next-line: completed-docs
  warning(msg: string, extra?: unknown): void;
}
