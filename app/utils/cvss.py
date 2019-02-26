
# -*- coding: utf-8 -*-
""" FluidIntegrates cvss auxiliar functions. """

from decimal import Decimal


def _calc_cvss2_temporal(severity, basescore):
    """Calculate cvss v2 temporal attribute."""
    temporal = Decimal(float(basescore) * severity['exploitability'] *
                       severity['resolutionLevel'] *
                       severity['confidenceLevel'], 1)
    resp = temporal.quantize(Decimal("0.1"))
    return resp


def _calc_cvss2_basescore(severity, parameters):
    """Calculate cvss v2 base score attribute."""
    impact = parameters['impact_factor'] * \
        (1 - ((1 - severity['confidentialityImpact']) *
              (1 - severity['integrityImpact']) *
              (1 - severity['availabilityImpact'])))
    f_impact_factor = get_f_impact(impact)
    exploitabilty = parameters['exploitability_factor'] * severity['accessComplexity'] * \
        severity['authentication'] * severity['accessVector']
    basescore = Decimal(((parameters['bs_factor_1'] * impact) -
                        parameters['bs_factor_3'] + (parameters['bs_factor_2'] *
                        exploitabilty)) * f_impact_factor)
    resp = basescore.quantize(Decimal("0.1"))
    return resp


def _calc_cvss2_environment(severity, parameters):
    """Calculate cvss v2 environment attribute."""
    exploitabilty = parameters['exploitability_factor'] * severity['accessComplexity'] * \
        severity['authentication'] * severity['accessVector']
    adj_impact = min(10, parameters['impact_factor'] *
                     (1 - (1 - severity['confidentialityImpact'] *
                           severity['confidentialityRequirement']) *
                     (1 - severity['integrityImpact'] *
                      severity['integrityRequirement']) *
                     (1 - severity['availabilityImpact'] *
                      severity['availabilityRequirement'])))
    f_impact_factor = get_f_impact(adj_impact)
    adj_basescore = ((parameters['bs_factor_1'] * adj_impact) -
                     parameters['bs_factor_3'] + (parameters['bs_factor_2'] *
                                                  exploitabilty)) * \
        f_impact_factor
    adj_temporal = round(adj_basescore * severity['exploitability'] *
                         severity['resolutionLevel'] *
                         severity['confidenceLevel'], 1)
    cvss_env = Decimal((adj_temporal + (10 - adj_temporal) *
                        severity['collateralDamagePotential']) *
                       severity['findingDistribution'])
    resp = cvss_env.quantize(Decimal("0.1"))
    return resp


def get_f_impact(impact):
    if impact:
        f_impact_factor = 1.176
    else:
        f_impact_factor = 0
    return f_impact_factor


def calculate_cvss_temporal(severity, basescore):
    """Calculate cvss temporal attribute."""
    cvss_temporal = _calc_cvss2_temporal(severity, basescore)
    return cvss_temporal


def calculate_cvss_basescore(severity, parameters):
    """Calculate cvss base score attribute."""
    cvss_basescore = _calc_cvss2_basescore(severity, parameters)
    return cvss_basescore


def calculate_cvss_enviroment(severity, parameters):
    """Calculate cvss environment attribute."""
    cvss_environment = _calc_cvss2_environment(severity, parameters)
    return cvss_environment
