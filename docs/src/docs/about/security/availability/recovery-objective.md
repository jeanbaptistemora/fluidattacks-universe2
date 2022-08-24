---
id: recovery-objective
title: Recovery Objective
sidebar_label: Recovery Objective
slug: /about/security/availability/recovery-objective
---

## Backups

Platform backups are always generated in full.

|   | Type      | Date                   | Hour    | Storage  |
|---|-----------|------------------------|---------|----------|
| 1 | Anual     | January 1st            | 6:30 am | 10 years |
| 2 | Monthly   | Every 1st of the month | 6:00 am | 1 year   |
| 3 | Weekly    | Every Saturday         | 5:30 am | 1 month  |
| 4 | Diary     | Everyday               | 5:00 am | 1 week   |
| 5 | Permanent | Every second           |         | 35 days  |

## Recovery objectives

| Objective                                        | Definition                                                                                                                                                                                                                                                                                                                                                                         | Time       | Description                                                                                                                                                                                        |
|--------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1. Recovery Time Objective (RTO)                 | Defines the maximum tolerable time limit within which the service must be restored to minimum acceptable conditions. If a disaster occurs and the service must be available immediately, the RTO is zero. However, if one hour of total service interruption is tolerated, the RTO is one hour.                                                                                    | 15 minutes | The platform is classified as critical so the backups are maintained on a permanent basis. The total restoration of a backup is done in 15 minutes, so this is the time it takes for the recovery. |
| 2. Recovery Point Objective (RPO)                | Defines the maximum tolerable data loss that can be accepted in a disaster situation. For example, if a disaster occurs and the backup of the information is weekly, it means that after recovering the service the data from one week before the incident will be available, the RPO is one week. If the backup is on-line and there is no acceptable data loss, the RPO is zero. | 0 minutes  | Considering that there are backups generated per second, the recovery target has 0.                                                                                                                |
| 3. Maximum Tolerable Period of Disruption (MTPD) | Defines the maximum time in which the service must operate normally before generating losses that cannot be assumed                                                                                                                                                                                                                                                                | 1 month    | The relationship between monthly operating costs and revenues is almost the same, so if the service is stopped completely for more than 1 month, the losses generated can be unsustainable.        |

## Impact over time

A service interruption can occur at any time;
however,
if it occurs at a certain point in time,
the severity of the interruption may be greater.
For this purpose,
the impact of an interruption on
the function at different moments
in time will be analyzed.

### Monthly analysis

In the monthly analysis,
the first and last month of
the year the ARM service
usage decreases due to platform
freezing and customer vacations.

| Month     | Impact |
|-----------|--------|
| January   | Medium |
| February  | High   |
| March     | High   |
| April     | High   |
| May       | High   |
| June      | High   |
| July      | High   |
| August    | High   |
| September | High   |
| October   | High   |
| November  | High   |
| December  | Medium |

### Weekly analysis

In weekly analysis the first
and last week of the month in
most of the cases there is the
closing or the beginning of
projects so the demand of the
service can increase.

| Week   | Impact |
|--------|--------|
| Week 1 | High   |
| Week 2 | Medium |
| Week 3 | Medium |
| Week 4 | High   |

### Daily analysis

During any day of the week there
can be a high impact from the
use of the service,
however most customers do
not work on weekends.

| Day       | Impact |
|-----------|--------|
| Monday    | High   |
| Tuesday   | High   |
| Wednesday | High   |
| Thursday  | High   |
| Friday    | High   |
| Saturday  | Low    |
| Sunday    | Low    |

### Hour analysis

The hours in which the customer
is during working hours are listed as high.

| Hour | Impact |
|------|--------|
| 0    | Low    |
| 1    | Low    |
| 2    | Low    |
| 3    | Low    |
| 4    | Low    |
| 5    | Low    |
| 6    | Low    |
| 7    | High   |
| 8    | High   |
| 9    | High   |
| 10   | High   |
| 11   | High   |
| 12   | Medium |
| 13   | Medium |
| 14   | High   |
| 15   | High   |
| 16   | High   |
| 17   | High   |
| 18   | High   |
| 19   | High   |
| 20   | Medium |
| 21   | Medium |
| 22   | Low    |
| 23   | Low    |
