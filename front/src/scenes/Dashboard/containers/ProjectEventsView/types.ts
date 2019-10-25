import { RouteComponentProps } from "react-router";

export type IEventViewBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

export interface IEventsViewStateProps extends RouteComponentProps {
  eventsDataset: Array<{ detail: string; eventDate: string; eventStatus: string; eventType: string; id: string }>;
  onClickRow: ((row: string | undefined) => JSX.Element);
  projectName: string;
}

export type IEventsViewProps = IEventViewBaseProps & IEventsViewStateProps;

export interface IEventsAttr {
  project: {
    events: Array<{
      detail: string;
      eventDate: string;
      eventStatus: string;
      eventType: string;
      id: string;
    }>;
  };
}
