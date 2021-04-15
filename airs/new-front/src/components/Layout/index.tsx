import React from "react";

import { Footer } from "../Footer";

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
