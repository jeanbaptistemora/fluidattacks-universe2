interface IEventEvidenceAttr {
  date: string;
  fileName: string;
  file?: FileList;
}

interface IGetEventEvidences {
  event: {
    eventStatus: string;
    evidences: {
      file1: IEventEvidenceAttr | null;
      image1: IEventEvidenceAttr | null;
      image2: IEventEvidenceAttr | null;
      image3: IEventEvidenceAttr | null;
      image4: IEventEvidenceAttr | null;
      image5: IEventEvidenceAttr | null;
      image6: IEventEvidenceAttr | null;
    };
    id: string;
  };
}

interface IUpdateEventEvidenceResultAttr {
  updateEventEvidence: {
    success: boolean;
  };
}

export type {
  IGetEventEvidences,
  IEventEvidenceAttr,
  IUpdateEventEvidenceResultAttr,
};
