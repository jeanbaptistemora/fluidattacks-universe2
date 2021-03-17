import { Footer } from "./Footer";
import React from "react";

interface IChildrenProps {
  children: JSX.Element;
}

const Layout: React.FC<IChildrenProps> = ({
  children,
}: IChildrenProps): JSX.Element => {
  return (
    <React.StrictMode>
      <div className={"bg-lightgray"}>
        <main>{children}</main>

        <Footer />
      </div>
    </React.StrictMode>
  );
};

export { Layout };
