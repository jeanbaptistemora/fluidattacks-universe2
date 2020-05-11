import pytest
from decimal import Decimal

from django.test import TestCase

from backend.utils import cvss, findings as finding_utils


class CvssTests(TestCase):

    @pytest.mark.no_changes_db
    def test_calculate_cvss2_basescore(self):
        severity = {'confidentialityImpact': 0, 'integrityImpact': 0.275,
                    'availabilityImpact': 0, 'accessComplexity': 0.61,
                    'authentication': 0.704, 'accessVector': 1
                    }
        cvss_version = '2'
        cvss_basescore = cvss.calculate_cvss_basescore(
            severity, finding_utils.CVSS_PARAMETERS['2'], cvss_version)
        cvss_basescore_test = Decimal(4.3).quantize(Decimal('0.1'))
        assert cvss_basescore == cvss_basescore_test

    @pytest.mark.no_changes_db
    def test_calculate_cvss2_temporal(self):
        severity = {'confidentialityImpact': 0, 'integrityImpact': 0.275,
                    'availabilityImpact': 0, 'accessComplexity': 0.61,
                    'authentication': 0.704, 'accessVector': 1,
                    'exploitability': 0.95, 'resolutionLevel': 0.95,
                    'confidenceLevel': 0.95
                    }
        cvss_version = '2'
        cvss_basescore = cvss.calculate_cvss_basescore(
            severity, finding_utils.CVSS_PARAMETERS['2'], cvss_version)
        cvss_temporal = cvss.calculate_cvss_temporal(
            severity, cvss_basescore, cvss_version)
        cvss_temporal_test = Decimal(3.7).quantize(Decimal('0.1'))
        assert cvss_temporal == cvss_temporal_test

    @pytest.mark.no_changes_db
    def test_calculate_cvss2_environment(self):
        severity = {'accessComplexity': 0.61, 'authentication': 0.704,
                    'accessVector': 1, 'confidentialityImpact': 0,
                    'confidentialityRequirement': 0.5, 'confidenceLevel': 0.95,
                    'integrityRequirement': 0.5, 'availabilityImpact': 0,
                    'availabilityRequirement': 0.5, 'findingDistribution': 0.25,
                    'resolutionLevel': 0.95, 'integrityImpact': 0.275,
                    'collateralDamagePotential': 0.1, 'exploitability': 0.95,
                    }
        cvss_version = '2'
        cvss_environment = cvss.calculate_cvss_environment(
            severity, finding_utils.CVSS_PARAMETERS['2'], cvss_version)
        cvss_environment_test = Decimal(0.9).quantize(Decimal('0.1'))
        assert cvss_environment == cvss_environment_test

    @pytest.mark.no_changes_db
    def test_calculate_cvss3_scope_changed_basescore(self):
        severity = {'confidentialityImpact': 0.22, 'integrityImpact': 0.22,
                    'availabilityImpact': 0, 'severityScope': 1,
                    'attackVector': 0.85, 'attackComplexity': 0.77,
                    'privilegesRequired': 0.68, 'userInteraction': 0.85
                    }
        cvss_version = '3.1'
        cvss_basescore = cvss.calculate_cvss_basescore(
            severity, finding_utils.CVSS_PARAMETERS['3.1'], cvss_version)
        cvss_basescore_test = Decimal(6.4).quantize(Decimal('0.1'))
        assert cvss_basescore == cvss_basescore_test

    @pytest.mark.no_changes_db
    def test_calculate_cvss3_scope_unchanged_basescore(self):
        severity = {'confidentialityImpact': 0.22, 'integrityImpact': 0.22,
                    'availabilityImpact': 0, 'severityScope': 0,
                    'attackVector': 0.85, 'attackComplexity': 0.77,
                    'privilegesRequired': 0.62, 'userInteraction': 0.85
                    }
        cvss_version = '3.1'
        cvss_basescore = cvss.calculate_cvss_basescore(
            severity, finding_utils.CVSS_PARAMETERS['3.1'], cvss_version)
        cvss_basescore_test = Decimal(5.4).quantize(Decimal('0.1'))
        assert cvss_basescore == cvss_basescore_test

    @pytest.mark.no_changes_db
    def test_calculate_cvss3_scope_changed_temporal(self):
        severity = {'confidentialityImpact': 0.22, 'integrityImpact': 0.22,
                    'availabilityImpact': 0, 'severityScope': 1,
                    'attackVector': 0.85, 'attackComplexity': 0.77,
                    'privilegesRequired': 0.68, 'userInteraction': 0.85,
                    'exploitability': 0.97, 'remediationLevel': 0.97,
                    'reportConfidence': 1
                    }
        cvss_version = '3.1'
        cvss_basescore = cvss.calculate_cvss_basescore(
            severity, finding_utils.CVSS_PARAMETERS['3.1'], cvss_version)
        cvss_temporal = cvss.calculate_cvss_temporal(
            severity, float(cvss_basescore), cvss_version)
        cvss_temporal_test = Decimal(6.1).quantize(Decimal('0.1'))
        assert cvss_temporal == cvss_temporal_test

    @pytest.mark.no_changes_db
    def test_calculate_cvss3_scope_unchanged_temporal(self):
        severity = {'confidentialityImpact': 0.22, 'integrityImpact': 0.22,
                    'availabilityImpact': 0, 'severityScope': 0,
                    'attackVector': 0.85, 'attackComplexity': 0.77,
                    'privilegesRequired': 0.62, 'userInteraction': 0.85,
                    'exploitability': 0.97, 'remediationLevel': 0.97,
                    'reportConfidence': 1
                    }
        cvss_version = '3.1'
        cvss_basescore = cvss.calculate_cvss_basescore(
            severity, finding_utils.CVSS_PARAMETERS['3.1'], cvss_version)
        cvss_temporal = cvss.calculate_cvss_temporal(
            severity, float(cvss_basescore), cvss_version)
        cvss_temporal_test = Decimal(5.1).quantize(Decimal('0.1'))
        assert cvss_temporal == cvss_temporal_test

    @pytest.mark.no_changes_db
    def test_calculate_cvss3_scope_changed_environment(self):
        severity = {'modifiedConfidentialityImpact': 0.22, 'reportConfidence': 1,
                    'modifiedIntegrityImpact': 0.22, 'modifiedAvailabilityImpact': 0.22,
                    'confidentialityRequirement': 0.5, 'integrityRequirement': 0.5,
                    'availabilityRequirement': 0.5, 'modifiedSeverityScope': 1,
                    'modifiedAttackVector': 0.85, 'modifiedAttackComplexity': 0.77,
                    'modifiedPrivilegesRequired': 0.68, 'remediationLevel': 0.97,
                    'exploitability': 0.97, 'modifiedUserInteraction': 0.85
                    }
        cvss_version = '3.1'
        cvss_environment = cvss.calculate_cvss_environment(
            severity, finding_utils.CVSS_PARAMETERS['3.1'], cvss_version)
        cvss_environment_test = Decimal(5.3).quantize(Decimal('0.1'))
        assert cvss_environment == cvss_environment_test

    @pytest.mark.no_changes_db
    def test_calculate_cvss3_scope_unchanged_environment(self):
        severity = {'modifiedConfidentialityImpact': 0.22, 'reportConfidence': 1,
                    'modifiedIntegrityImpact': 0.22, 'modifiedAvailabilityImpact': 0.22,
                    'confidentialityRequirement': 0.5, 'integrityRequirement': 0.5,
                    'availabilityRequirement': 0.5, 'modifiedSeverityScope': 0,
                    'modifiedAttackVector': 0.85, 'modifiedAttackComplexity': 0.77,
                    'modifiedPrivilegesRequired': 0.62, 'remediationLevel': 0.97,
                    'exploitability': 0.97, 'modifiedUserInteraction': 0.85
                    }
        cvss_version = '3.1'
        cvss_environment = cvss.calculate_cvss_environment(
            severity, finding_utils.CVSS_PARAMETERS['3.1'], cvss_version)
        cvss_environment_test = Decimal(4.6).quantize(Decimal('0.1'))
        assert cvss_environment == cvss_environment_test
