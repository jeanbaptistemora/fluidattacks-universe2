import type React from "react";
import { createContext, useContext } from "react";

interface ISessionTokenContext
  extends Array<React.Dispatch<React.SetStateAction<string>> | string> {
  0: string;
  1: React.Dispatch<React.SetStateAction<string>>;
}

const SessionToken = createContext<ISessionTokenContext>([
  "",
  (): void => undefined,
]);
const useSessionToken = (): ISessionTokenContext =>
  useContext<ISessionTokenContext>(SessionToken);

export { SessionToken, ISessionTokenContext, useSessionToken };
