import { faClipboard, faPencilAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback } from "react";

import { Button } from "components/Button";

const SecretValue: React.FC<{
  secretDescription: string;
  secretKey: string;
  secretValue: string;
  onEdit: (key: string, value: string, description: string) => void;
}> = ({
  secretDescription,
  secretKey,
  secretValue,
  onEdit,
}: {
  secretDescription: string;
  secretKey: string;
  secretValue: string;
  onEdit: (key: string, value: string, description: string) => void;
}): JSX.Element => {
  function handleOnEdit(): void {
    onEdit(secretKey, secretValue, secretDescription);
  }

  return (
    <div>
      {"*********************"}
      <Button
        id={"copy-secret"}
        onClick={useCallback(async (): Promise<void> => {
          const { clipboard } = navigator;

          await clipboard.writeText(secretValue);
          document.execCommand("copy");
        }, [secretValue])}
        variant={"secondary"}
      >
        <FontAwesomeIcon icon={faClipboard} />
      </Button>
      <Button id={"edit-secret"} onClick={handleOnEdit} variant={"secondary"}>
        <FontAwesomeIcon icon={faPencilAlt} />
      </Button>
    </div>
  );
};

export { SecretValue };
