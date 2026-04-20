from dataclasses import dataclass


@dataclass
class Scenario:
    name: str
    education_investment: float
    computation_policy: float
    efficiency: float
    corruption: float
    risk: float
    economic_freedom: float
    innovation_incentive: float
    policy_stability: float
    teacher_training: float
    accountability: float
    financial_recognition: float
    state_policy: float
    family_support_mean: float
    school_management: float
    bureaucracy: float


SCENARIOS = [
    Scenario(
        name="Baseline_sem_computacao",
        education_investment=1.00,
        computation_policy=0.00,
        efficiency=0.55,
        corruption=0.45,
        risk=0.45,
        economic_freedom=0.50,
        innovation_incentive=0.45,
        policy_stability=0.45,
        teacher_training=0.45,
        accountability=0.35,
        financial_recognition=0.35,
        state_policy=0.35,
        family_support_mean=0.50,
        school_management=0.50,
        bureaucracy=0.50,
    ),
    Scenario(
        name="Computacao_superficial",
        education_investment=1.05,
        computation_policy=0.45,
        efficiency=0.58,
        corruption=0.40,
        risk=0.40,
        economic_freedom=0.52,
        innovation_incentive=0.50,
        policy_stability=0.48,
        teacher_training=0.42,
        accountability=0.40,
        financial_recognition=0.38,
        state_policy=0.42,
        family_support_mean=0.50,
        school_management=0.52,
        bureaucracy=0.48,
    ),
    Scenario(
        name="Computacao_estruturada",
        education_investment=1.20,
        computation_policy=0.90,
        efficiency=0.75,
        corruption=0.20,
        risk=0.20,
        economic_freedom=0.72,
        innovation_incentive=0.78,
        policy_stability=0.82,
        teacher_training=0.82,
        accountability=0.70,
        financial_recognition=0.68,
        state_policy=0.85,
        family_support_mean=0.54,
        school_management=0.72,
        bureaucracy=0.25,
    ),
    Scenario(
        name="Boa_educacao_mau_ambiente_institucional",
        education_investment=1.20,
        computation_policy=0.90,
        efficiency=0.52,
        corruption=0.55,
        risk=0.62,
        economic_freedom=0.35,
        innovation_incentive=0.42,
        policy_stability=0.40,
        teacher_training=0.78,
        accountability=0.55,
        financial_recognition=0.55,
        state_policy=0.45,
        family_support_mean=0.54,
        school_management=0.65,
        bureaucracy=0.62,
    ),
    Scenario(
        name="Ciclo_virtuoso_completo",
        education_investment=1.35,
        computation_policy=1.00,
        efficiency=0.88,
        corruption=0.08,
        risk=0.10,
        economic_freedom=0.88,
        innovation_incentive=0.92,
        policy_stability=0.92,
        teacher_training=0.90,
        accountability=0.82,
        financial_recognition=0.80,
        state_policy=0.95,
        family_support_mean=0.58,
        school_management=0.82,
        bureaucracy=0.12,
    ),
    Scenario(
        name="Muito_gasto_pouca_eficiencia",
        education_investment=1.60,
        computation_policy=0.80,
        efficiency=0.38,
        corruption=0.50,
        risk=0.48,
        economic_freedom=0.46,
        innovation_incentive=0.52,
        policy_stability=0.46,
        teacher_training=0.62,
        accountability=0.42,
        financial_recognition=0.44,
        state_policy=0.40,
        family_support_mean=0.52,
        school_management=0.55,
        bureaucracy=0.58,
    ),
]


