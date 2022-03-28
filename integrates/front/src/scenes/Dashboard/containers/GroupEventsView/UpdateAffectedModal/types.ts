import type { IEventsDataset } from "..";
import type { IFindingsQuery } from "../AffectedReattackAccordion/types";

interface IUpdateAffectedValues {
  eventId: string;
  affectedReattacks: string[];
}

interface IUpdateAffectedModalProps {
  eventsInfo: IEventsDataset;
  findingsInfo: IFindingsQuery;
  onClose: () => void;
  onSubmit: (values: IUpdateAffectedValues) => Promise<void>;
}

export { IUpdateAffectedValues, IUpdateAffectedModalProps };
