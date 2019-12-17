import React from "react";
import { default as loadingAnim } from "../../resources/loading.gif";
import { default as style } from "./index.css";

const preloader: React.FC = (): JSX.Element => (
  <React.StrictMode>
    <div id="full_loader" className={style.loader}>
      <img src={loadingAnim} width="100" height="100" />
    </div>
  </React.StrictMode>
);

export { preloader as Preloader };
