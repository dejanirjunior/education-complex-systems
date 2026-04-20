import random
from typing import Dict, List

import numpy as np
import pandas as pd

from scenarios import Scenario


class Student:
    def __init__(self, family_support_mean: float):
        self.ability = float(np.clip(np.random.normal(0.55, 0.15), 0.10, 1.00))
        self.motivation = float(np.clip(np.random.normal(0.60, 0.18), 0.10, 1.00))
        self.family_support = float(np.clip(np.random.normal(family_support_mean, 0.15), 0.00, 1.00))
        self.knowledge = float(np.clip(np.random.normal(0.20, 0.05), 0.05, 0.50))
        self.computational_thinking = 0.0


class Teacher:
    def __init__(self, training_factor: float, financial_recognition: float, accountability: float):
        self.teaching_quality = float(np.clip(np.random.normal(0.55, 0.12), 0.20, 1.00))
        self.tech_training = float(np.clip(np.random.normal(training_factor, 0.10), 0.10, 1.00))
        self.incentive_response = float(
            np.clip(
                0.5 * financial_recognition + 0.5 * accountability + np.random.normal(0.0, 0.08),
                0.00,
                1.00,
            )
        )


class School:
    def __init__(self, management: float, scenario: Scenario):
        self.infrastructure = float(np.clip(np.random.normal(0.55, 0.12), 0.20, 1.00))
        self.management_quality = float(np.clip(np.random.normal(management, 0.10), 0.10, 1.00))
        self.computation_intensity = scenario.computation_policy
        self.accountability = scenario.accountability


class Company:
    def __init__(self):
        self.innovation_level = float(np.clip(np.random.normal(0.35, 0.08), 0.05, 0.90))
        self.talent_absorption = float(np.clip(np.random.normal(0.60, 0.10), 0.20, 1.00))
        self.productivity = float(np.clip(np.random.normal(1.00, 0.05), 0.70, 1.30))


class Economy:
    def __init__(self):
        self.productivity = 1.0
        self.capital_attraction = 1.0
        self.innovation_capacity = 0.5


class Government:
    def __init__(self, scenario: Scenario):
        self.education_investment = scenario.education_investment
        self.computation_policy = scenario.computation_policy
        self.efficiency = scenario.efficiency
        self.corruption = scenario.corruption
        self.risk = scenario.risk
        self.economic_freedom = scenario.economic_freedom
        self.innovation_incentive = scenario.innovation_incentive
        self.policy_stability = scenario.policy_stability
        self.teacher_training = scenario.teacher_training
        self.accountability = scenario.accountability
        self.financial_recognition = scenario.financial_recognition
        self.state_policy = scenario.state_policy
        self.bureaucracy = scenario.bureaucracy


class Simulation:
    def __init__(
        self,
        scenario: Scenario,
        n_students: int = 1200,
        n_teachers: int = 60,
        n_schools: int = 30,
        n_companies: int = 80,
        years: int = 20,
        seed: int = 42,
    ):
        np.random.seed(seed)
        random.seed(seed)

        self.scenario = scenario
        self.years = years

        self.students = [Student(scenario.family_support_mean) for _ in range(n_students)]
        self.teachers = [
            Teacher(
                training_factor=scenario.teacher_training,
                financial_recognition=scenario.financial_recognition,
                accountability=scenario.accountability,
            )
            for _ in range(n_teachers)
        ]
        self.schools = [School(scenario.school_management, scenario) for _ in range(n_schools)]
        self.companies = [Company() for _ in range(n_companies)]

        self.government = Government(scenario)
        self.economy = Economy()

        self.history: List[Dict[str, float]] = []

    def institutional_quality(self) -> float:
        positive = (
            self.government.efficiency
            + self.government.economic_freedom
            + self.government.innovation_incentive
            + self.government.policy_stability
            + self.government.teacher_training
            + self.government.accountability
            + self.government.financial_recognition
            + self.government.state_policy
        ) / 8.0

        negative = (
            self.government.corruption
            + self.government.risk
            + self.government.bureaucracy
        ) / 3.0

        return float(np.clip(positive - 0.65 * negative + 0.35, 0.0, 1.5))

    def update_education(self):
        iq = self.institutional_quality()

        avg_school_quality = np.mean(
            [
                0.35 * school.infrastructure
                + 0.45 * school.management_quality
                + 0.20 * school.accountability
                for school in self.schools
            ]
        )

        for student in self.students:
            teacher = random.choice(self.teachers)

            effective_investment = (
                self.government.education_investment
                * self.government.efficiency
                * (1 - 0.75 * self.government.corruption)
            )

            learning = (
                0.09
                * student.ability
                * student.motivation
                * (0.35 + student.family_support)
                * (0.45 + teacher.teaching_quality)
                * (0.35 + teacher.incentive_response)
                * (0.35 + avg_school_quality)
                * (0.35 + effective_investment)
                * (0.30 + iq)
            )

            noise = np.random.normal(0.0, 0.006)

            student.knowledge = float(np.clip(student.knowledge + learning + noise, 0.0, 5.0))

            student.motivation = float(
                np.clip(
                    student.motivation + 0.01 * learning - 0.002 + np.random.normal(0.0, 0.003),
                    0.05,
                    1.0,
                )
            )

    def update_computational_thinking(self):
        iq = self.institutional_quality()
        avg_teacher_tech = np.mean([teacher.tech_training for teacher in self.teachers])
        avg_school_compute = np.mean([school.computation_intensity for school in self.schools])

        policy_effect = (
            self.government.computation_policy
            * self.government.policy_stability
            * self.government.state_policy
            * (0.5 + avg_teacher_tech)
            * (0.5 + avg_school_compute)
            * (0.5 + iq)
        )

        for student in self.students:
            delta = (
                0.03
                * policy_effect
                * (0.6 + student.knowledge)
                * (0.4 + student.motivation)
            )

            noise = np.random.normal(0.0, 0.004)

            student.computational_thinking = float(
                np.clip(student.computational_thinking + delta + noise, 0.0, 5.0)
            )

    def update_innovation_and_companies(self):
        avg_knowledge = np.mean([student.knowledge for student in self.students])
        avg_comp = np.mean([student.computational_thinking for student in self.students])
        iq = self.institutional_quality()

        talent_supply = 0.55 * avg_knowledge + 0.45 * avg_comp

        business_environment = (
            self.government.economic_freedom
            * self.government.innovation_incentive
            * (1 - 0.5 * self.government.bureaucracy)
            * (1 - 0.4 * self.government.risk)
            * (0.5 + iq)
        )

        for company in self.companies:
            company_gain = (
                0.025
                * talent_supply
                * company.talent_absorption
                * business_environment
            )
            company_gain += np.random.normal(0.0, 0.003)

            company.innovation_level = float(np.clip(company.innovation_level + company_gain, 0.0, 5.0))
            company.productivity = float(
                np.clip(company.productivity + 0.012 * company.innovation_level + 0.004 * talent_supply, 0.5, 8.0)
            )

    def update_economy(self):
        avg_company_innovation = np.mean([company.innovation_level for company in self.companies])
        avg_company_productivity = np.mean([company.productivity for company in self.companies])
        iq = self.institutional_quality()

        productivity_gain = (
            0.02
            * avg_company_innovation
            * avg_company_productivity
            * (0.45 + iq)
            * (1 - 0.45 * self.government.corruption)
            * (1 - 0.35 * self.government.risk)
        )

        capital_gain = (
            0.018
            * self.economy.productivity
            * (0.55 + self.government.economic_freedom)
            * (0.55 + avg_company_innovation)
            * (1 - 0.55 * self.government.risk)
            * (1 - 0.35 * self.government.corruption)
        )

        innovation_gain = (
            0.01
            * avg_company_innovation
            * (0.55 + self.government.innovation_incentive)
            * (0.5 + iq)
        )

        self.economy.productivity = float(np.clip(self.economy.productivity + productivity_gain, 0.5, 10.0))
        self.economy.capital_attraction = float(np.clip(self.economy.capital_attraction + capital_gain, 0.5, 10.0))
        self.economy.innovation_capacity = float(np.clip(self.economy.innovation_capacity + innovation_gain, 0.1, 10.0))

    def reinvest(self):
        reinvestment = (
            0.02
            * self.economy.productivity
            * self.economy.capital_attraction
            * self.government.efficiency
            * self.government.state_policy
            * (1 - 0.6 * self.government.corruption)
        )

        self.government.education_investment = float(
            np.clip(self.government.education_investment + reinvestment, 0.2, 5.0)
        )

    def collect_metrics(self, year: int):
        knowledge = np.array([student.knowledge for student in self.students])
        computational = np.array([student.computational_thinking for student in self.students])

        pisa_like = np.clip(250 + 80 * knowledge.mean() + 55 * computational.mean(), 200, 800)
        inequality_cv = float(knowledge.std() / max(knowledge.mean(), 1e-6))
        tech_ready_share = float(np.mean((knowledge > 2.0) & (computational > 1.2)))

        effective_spending = (
            self.government.education_investment
            * self.government.efficiency
            * (1 - 0.75 * self.government.corruption)
        )

        spending_loss = max(self.government.education_investment - effective_spending, 0.0)
        institutional_quality = self.institutional_quality()

        self.history.append(
            {
                "scenario": self.scenario.name,
                "year": year,
                "avg_knowledge": knowledge.mean(),
                "avg_computational": computational.mean(),
                "pisa_like": pisa_like,
                "inequality_cv": inequality_cv,
                "tech_ready_share": tech_ready_share,
                "economy_productivity": self.economy.productivity,
                "capital_attraction": self.economy.capital_attraction,
                "innovation_capacity": self.economy.innovation_capacity,
                "education_investment": self.government.education_investment,
                "effective_spending": effective_spending,
                "spending_loss": spending_loss,
                "institutional_quality": institutional_quality,
            }
        )

    def run(self) -> pd.DataFrame:
        for year in range(self.years + 1):
            if year > 0:
                self.update_education()
                self.update_computational_thinking()
                self.update_innovation_and_companies()
                self.update_economy()
                self.reinvest()

            self.collect_metrics(year)

        return pd.DataFrame(self.history)

