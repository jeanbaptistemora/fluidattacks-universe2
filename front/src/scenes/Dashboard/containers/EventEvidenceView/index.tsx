/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import _ from "lodash";
import React from "react";
import { Query, QueryResult } from "react-apollo";
import { RouteComponentProps } from "react-router";
import { evidenceImage as EvidenceImage } from "../../components/EvidenceImage/index";
import { GET_EVENT_EVIDENCES } from "./queries";

type EventEvidenceProps = RouteComponentProps<{ eventId: string; projectName: string }>;

const eventEvidenceView: React.FC<EventEvidenceProps> = (props: EventEvidenceProps): JSX.Element => {
  const { eventId } = props.match.params;

  const emptyImage: string = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
  );

  const handleClick: (() => void) = (): void => undefined;
  const baseUrl: string = window.location.href.replace("dashboard#!", "");

  return (
    <React.StrictMode>
      <Query query={GET_EVENT_EVIDENCES} variables={{ eventId }}>
        {({ data, loading }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || loading) { return <React.Fragment />; }

          return (
            <EvidenceImage
              description="Evidence"
              isDescriptionEditable={false}
              isEditing={false}
              name="evidence"
              onClick={handleClick}
              onUpdate={handleClick}
              url={_.isEmpty(data.event.evidence) ? emptyImage : `${baseUrl}/${data.event.evidence}`}
            />
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

export { eventEvidenceView as EventEvidenceView };
