/* eslint-disable fp/no-this, fp/no-class */

import type { ErrorInfo, ReactNode } from "react";
import React, { Component } from "react";

import { Logger } from "utils/logger";

interface IProps {
  children: ReactNode;
}

interface IState {
  hasError: boolean;
}

// Error Booundary at the time of this commit NEEDS to be a class component
class ErrorBoundary extends Component<IProps, IState> {
  // eslint-disable-next-line react/sort-comp, react/state-in-constructor
  public state: IState = {
    hasError: false,
  };

  public static getDerivedStateFromError(_: Error): IState {
    // Update state so the next render will show the fallback UI.
    return { hasError: true };
  }

  public shouldComponentUpdate(_prevProps: IProps, prevState: IState): boolean {
    const { hasError } = this.state;
    if (prevState.hasError !== hasError) {
      return true;
    }

    return false;
  }

  // eslint-disable-next-line class-methods-use-this
  public componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    Logger.error(
      `Uncaught error: ${error.name}
      ${error.message}
      ${error.stack ?? ""}
      ${errorInfo.componentStack}`
    );
  }

  public render(): ReactNode {
    const { hasError } = this.state;
    const { children } = this.props;

    if (hasError) {
      return <h1>{"Sorry.. there was an error"}</h1>;
    }

    return children;
  }
}

export { ErrorBoundary };
