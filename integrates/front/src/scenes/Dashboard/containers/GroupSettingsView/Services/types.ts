/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IFormData {
  asm: boolean;
  comments: string;
  confirmation: string;
  description: string;
  forces?: boolean;
  language: string;
  machine: boolean;
  reason: string;
  organization?: string;
  service: string;
  squad: boolean;
  type: string;
}

interface IGroupData {
  group: {
    businessId: string;
    businessName: string;
    description: string;
    hasSquad: boolean;
    hasForces: boolean;
    hasMachine: boolean;
    language: string;
    managed: string;
    organization: {
      name: string;
    };
    service: string;
    sprintDuration: string;
    sprintStartDate: string;
    subscription: string;
  };
}

interface IServicesProps {
  groupName: string;
}

interface IServicesFormProps {
  data: IGroupData | undefined;
  groupName: string;
  isModalOpen: boolean;
  loadingGroupData: boolean;
  setIsModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  submittingGroupData: boolean;
}

interface IServicesDataSet {
  id: string;
  onChange?: (checked: boolean) => void;
  service: string;
}

export type {
  IFormData,
  IGroupData,
  IServicesDataSet,
  IServicesFormProps,
  IServicesProps,
};
