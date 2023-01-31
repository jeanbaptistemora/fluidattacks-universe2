import React from "react";
import { MemoryRouter, Route, Routes } from "react-router-dom";

import { ToeLines } from "./containers/ToeLines";

import "./styles.css";

const App = (): JSX.Element => {
  return (
    <div className={"app"}>
      <MemoryRouter initialEntries={["/toeLines"]}>
        <Routes>
          <Route element={<ToeLines />} path={"toeLines"} />
        </Routes>
      </MemoryRouter>
    </div>
  );
};

export { App };
