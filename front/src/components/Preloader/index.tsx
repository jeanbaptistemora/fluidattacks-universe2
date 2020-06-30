import React from "react";
import { default as loadingAnim } from "../../resources/loading.gif";
import { default as style } from "./index.css";

export const Preloader: React.FC = (): JSX.Element => (
  <div className={style.loader} id={"full_loader"}>
    <img height={"100"} src={loadingAnim} width={"100"} />
  </div>
);
