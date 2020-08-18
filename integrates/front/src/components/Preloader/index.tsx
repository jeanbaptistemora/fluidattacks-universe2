import React from "react";
import loadingAnim from "../../resources/loading.gif";
import style from "./index.css";

export const Preloader: React.FC = (): JSX.Element => (
  <div className={style.loader} id={"full_loader"}>
    <img
      alt={"Loading animation"}
      height={"100"}
      src={loadingAnim}
      width={"100"}
    />
  </div>
);
