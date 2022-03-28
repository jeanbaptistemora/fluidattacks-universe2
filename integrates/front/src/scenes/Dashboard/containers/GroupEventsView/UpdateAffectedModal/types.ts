import type { IEventsDataset } from "..";
import type { IFinding } from "../AffectedReattackAccordion/types";

interface IUpdateAffectedValues {
  eventId: string;
  affectedReattacks: string[];
}

interface IUpdateAffectedModalProps {
  eventsInfo: IEventsDataset | undefined;
  findings: IFinding[];
  onClose: () => void;
  onSubmit: (values: IUpdateAffectedValues) => Promise<void>;
}

export { IUpdateAffectedValues, IUpdateAffectedModalProps };
