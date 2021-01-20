import React from "react";

interface IUser {
  userEmail: string;
  userName: string;
}

interface IAuthContext extends IUser {
  setUser?: React.Dispatch<React.SetStateAction<IUser>>;
}

const authContext: React.Context<IAuthContext> = React.createContext({
  userEmail: "",
  userName: "",
});

export { authContext, IAuthContext };
