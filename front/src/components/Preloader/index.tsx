import React from "react";
import { default as style } from "./index.css";

const preloader: React.FC = (): JSX.Element => (
  <React.StrictMode>
    <div id="full_loader" className={style.loader}>
      <img src="assets/img/loading.gif" width="100" height="100" />
    </div>
  </React.StrictMode>
);

export { preloader as Preloader };
