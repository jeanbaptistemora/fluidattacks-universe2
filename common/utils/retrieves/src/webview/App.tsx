import { messageHandler } from "@estruyf/vscode/dist/client";
import { useCallback, useState } from "react";
// eslint-disable-next-line import/no-extraneous-dependencies, import/no-namespace
import * as React from "react";
import "./styles.css";

const App = (): JSX.Element => {
  const [message, setMessage] = useState<string>("");
  const [error, setError] = useState<string>("");

  const sendMessage = useCallback((): void => {
    messageHandler.send("POST_DATA", { msg: "Hello from the webview" });
  }, []);

  const requestData = useCallback((): void => {
    void messageHandler.request<string>("GET_DATA").then((msg): void => {
      setMessage(msg);
    });
  }, []);

  const requestWithErrorData = useCallback((): void => {
    messageHandler
      .request<string>("GET_DATA_ERROR")
      .then((msg): void => {
        setMessage(msg);
      })
      .catch((err): void => {
        setError(err);
      });
  }, []);

  return (
    <div className={"app"}>
      <h1>{"Hello from the React Webview Starter"}</h1>

      <div className={"app__actions"}>
        <button onClick={sendMessage}>{"Send message to extension"}</button>

        <button onClick={requestData}>{"Get data from extension"}</button>

        <button onClick={requestWithErrorData}>{"Get data with error"}</button>
      </div>

      {message && (
        <p>
          <strong>{"Message from the extension"}</strong>

          {":"}

          {message}
        </p>
      )}

      {error && (
        <p className={"app__error"}>
          <strong>{"ERROR"}</strong>

          {":"}

          {error}
        </p>
      )}
    </div>
  );
};

export { App };
