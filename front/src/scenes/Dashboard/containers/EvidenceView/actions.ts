import * as actionTypes from "./actionTypes";

export interface IActionStructure {
  /* tslint:disable-next-line:no-any
   * Disabling this rule is necessary because the payload
   * type may differ between actions
   */
  payload: any;
  type: string;
}

export const openEvidence: ((imgIndex: number) => IActionStructure) =
  (imgIndex: number): IActionStructure => ({
    payload: { imgIndex },
    type: actionTypes.OPEN_EVIDENCE,
  });

export const closeEvidence: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_EVIDENCE,
  });

export const moveEvidenceIndex:
  ((currentIndex: number, totalImages: number, direction: "next" | "previous") => IActionStructure) =
  (currentIndex: number, totalImages: number, direction: "next" | "previous"): IActionStructure => ({
    payload: {
      index: (direction === "next" ? (currentIndex + 1) : (currentIndex + totalImages - 1))
        % totalImages,
    },
    type: actionTypes.MOVE_EVIDENCE,
  });

export const editEvidence: ((value: boolean) => IActionStructure) =
  (value: boolean): IActionStructure => ({
    payload: { value },
    type: actionTypes.EDIT_EVIDENCE,
  });

export const clearEvidence: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLEAR_EVIDENCE,
  });
