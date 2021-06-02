interface IUpdateForcesTokenAttr {
  updateForcesAccessToken: {
    sessionJwt: string;
    success: boolean;
  };
}

interface IGetForcesTokenAttr {
  group: {
    forcesToken: string | undefined;
  };
}

export { IUpdateForcesTokenAttr, IGetForcesTokenAttr };
