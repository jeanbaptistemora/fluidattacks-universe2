interface IUpdateForcesTokenAttr {
  updateAccessToken: {
    sessionJwt: string;
    success: boolean;
  };
}

interface IGetForcesTokenAttr {
  project: {
    forcesToken: string | undefined;
  };
}

export { IUpdateForcesTokenAttr, IGetForcesTokenAttr };
