import React from "react";
import style from "./index.css";

const preloader: React.StatelessComponent =
 (): JSX.Element => (
  <React.StrictMode>
    <div id="full_loader" className={style.loader}>
      <p className={style.text}>
        <img
          src="assets/img/loading.gif"
          width="120"
          height="120"
        />
        <br/>
        Powered by <b>Fluid Attacks</b>
      </p>
    </div>
  </React.StrictMode>
);

export = preloader;
