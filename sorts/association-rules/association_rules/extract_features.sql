WITH vulnerabilities AS (
SELECT "Integrates Vms"."finding_id_str" AS "Finding Id Str",
       "Integrates Vms"."id_str" AS "Uuid Str",
       CASE WHEN CHARINDEX(' ', "Integrates Vms"."where_str") > 0
       THEN SUBSTRING("Integrates Vms"."where_str", 1, CHARINDEX(' ', "Integrates Vms"."where_str")-1) 
       ELSE "Integrates Vms"."where_str" END AS "Where Str",
       "Integrates Vms"."where_str" AS "Raw_File",
       "Integrates Vms"."specific_str" AS "Specific Str",
       "Integrates Vms"."type_str" AS "Vuln Type Str",
       "Integrates Vms"."repo_str" AS "Repo Nickname Str",
       "Integrates Vms"."bug_tracking_system_url_str" AS "External_bts Str",
       "Integrates Vms"."commit_str" AS "Commit Str",
       "Integrates Vms"."root_id_str" AS "Root Id Str",
       "Integrates Vms"."integrates_vms____tags_str" AS "Vulnerability Tag",
       "Integrates Vms"."integrates_vms____stream_str" AS "Integrates Vms Stream Str",
       "Integrates Vms"."skims_method_str" AS "Skims Method str",
       "Integrates Vms"."developer_str" AS "Developer Str"
FROM "dynamodb"."integrates_vms" AS "Integrates Vms"
WHERE ("Integrates Vms"."pk_str" LIKE 'VULN#%'
       AND "Integrates Vms"."sk_str" LIKE 'FIN#%')
),

findings AS (
SELECT vms.severity__integrity_impact_float,
        vms.severity__user_interaction_float,
        vms.severity__modified_integrity_impact_float,
        vms.sorts_str,
        vms.affected_systems_str,
        vms.severity__severity_scope_float,
        vms.evidences__exploitation__url_str,
        vms.compromised_attributes_str,
        vms.severity__report_confidence_float,
        vms.description_str,
        vms.cvss_version_str,
        vms.analyst_email_str,
        vms.group_name_str,
        vms.attack_vector_description_str,
        vms.severity__modified_privileges_required_float,
        vms.recommendation_str,
        vms.severity__availability_requirement_float,
        vms.title_str,
        vms.requirements_str,
        vms.severity__exploitability_float,
        vms.severity__attack_complexity_float,
        vms.severity__modified_attack_vector_float,
        vms.severity__modified_severity_scope_float,
        vms.threat_str,
        vms.severity__modified_confidentiality_impact_float,
        vms.severity__attack_vector_float,
        vms.sk_str,
        vms.severity__confidentiality_impact_float,
        vms.id_str,
        vms.severity__remediation_level_float,
        vms.severity__integrity_requirement_float,
        vms.pk_str,
        vms.severity__privileges_required_float,
        vms.severity__modified_attack_complexity_float,
        vms.severity__availability_impact_float,
        vms.severity__confidentiality_requirement_float
FROM "dynamodb"."integrates_vms" AS vms
WHERE vms.pk_str LIKE 'FIN#%' AND
vms.sk_str LIKE 'GROUP#%' AND
vms.title_str IS NOT NULL
),

findings_historic_state AS (
SELECT 
        ROW_NUMBER() OVER(PARTITION BY vms.pk_str ORDER BY vms.modified_date_datetime ASC)-1 AS forward_index_int,
        ROW_NUMBER() OVER(PARTITION BY vms.pk_str ORDER BY vms.modified_date_datetime DESC)-1 AS backward_index_int,
        vms.modified_date_datetime,
        vms.justification_str,
        vms.source_str,
        vms.modified_by_str,
        vms.status_str,
        SUBSTRING(vms.pk_str, 5) AS id_str
FROM "dynamodb"."integrates_vms" AS vms
WHERE vms.pk_str LIKE 'FIN#%'
AND vms.sk_str LIKE 'STATE#%'
),

v AS (
  SELECT "Integrates Vms"."finding_id_str" AS "Finding Id Str",
       "Integrates Vms"."id_str" AS "Uuid Str",
       "Integrates Vms"."where_str" AS "Where Str",
       "Integrates Vms"."specific_str" AS "Specific Str",
       "Integrates Vms"."type_str" AS "Vuln Type Str",
       "Integrates Vms"."repo_str" AS "Repo Nickname Str",
       "Integrates Vms"."bug_tracking_system_url_str" AS "External_bts Str",
       "Integrates Vms"."commit_str" AS "Commit Str",
       "Integrates Vms"."root_id_str" AS "Root Id Str"
FROM "dynamodb"."integrates_vms" AS "Integrates Vms"
WHERE ("Integrates Vms"."pk_str" LIKE 'VULN#%'
       AND "Integrates Vms"."sk_str" LIKE 'FIN#%')
  ),
  
s AS (SELECT * FROM(
SELECT 
        ROW_NUMBER() OVER(PARTITION BY "Integrates Vms"."pk_str" ORDER BY "Integrates Vms"."modified_date_datetime" ASC)-1 AS "Forward Index Int",
        ROW_NUMBER() OVER(PARTITION BY "Integrates Vms"."pk_str" ORDER BY "Integrates Vms"."modified_date_datetime" DESC)-1 AS "Backward Index Int",
        SUBSTRING("Integrates Vms"."pk_str", 6) AS "Uuid",
        "Integrates Vms"."modified_by_str" AS "Email Str",
        ("Integrates Vms"."modified_date_datetime" AT TIME ZONE 'UTC') AS "Date Datetime",
        "Integrates Vms"."status_str" AS "Status Str",
        "Integrates Vms"."comment_id_str" AS "Comment Id Str"
FROM "dynamodb"."integrates_vms" AS "Integrates Vms"
WHERE ("Integrates Vms"."pk_str" LIKE 'VULN#%'
       AND "Integrates Vms"."sk_str" LIKE 'ZERORISK#%')) prov
    WHERE prov."Backward Index Int" = 0
),

vulnerabilities_ZR AS (
SELECT 
    COALESCE(v."Uuid Str", s."Uuid") AS "Uuid Str", 
    COALESCE(s."Status Str", 'NOT REQUESTED') AS "Status Str"
FROM v FULL OUTER JOIN s
ON v."Uuid Str" = s."Uuid"
),

group_company AS (
SELECT SUBSTRING(organizations.sk_str, 6) AS company,
       SUBSTRING(organizations2.sk_str, 7) AS group_name
FROM dynamodb.fi_organizations AS organizations
INNER JOIN
  (SELECT *
   FROM dynamodb.fi_organizations AS organizations_temp
   WHERE organizations_temp.sk_str ILIKE 'group%') AS organizations2 ON organizations.pk_str = organizations2.pk_str
WHERE organizations.sk_str ILIKE 'info%'
),


findings_last_state AS (
SELECT f.id_str, f.title_str, f.group_name_str
FROM findings f 
    INNER JOIN (SELECT * FROM findings_historic_state WHERE backward_index_int = 0 AND status_str = 'APPROVED') h
    on f.id_str = h.id_str    
),

vuln_find AS (
SELECT v."Uuid Str", v."Where Str", v."Raw_File", v."Finding Id Str", f.title_str, f.group_name_str
FROM vulnerabilities v INNER JOIN findings_last_state f
ON v."Finding Id Str" = f.id_str
WHERE v."Vuln Type Str" = 'LINES'
),

vulns_enriched AS (
SELECT vuln.*, zr."Status Str" FROM vuln_find AS vuln
INNER JOIN (SELECT * FROM vulnerabilities_ZR WHERE "Status Str" != 'CONFIRMED') zr
ON vuln."Uuid Str" = zr."Uuid Str"
),

definitive AS (
SELECT vulns.*, g.company 
FROM vulns_enriched vulns 
INNER JOIN (SELECT * FROM group_company WHERE "company" NOT IN ('imamura', 'okada', 'orgtest')) g
ON vulns.group_name_str = g.group_name
)

SELECT * FROM definitive
