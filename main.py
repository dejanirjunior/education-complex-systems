import os

import matplotlib.pyplot as plt
import pandas as pd

from scenarios import SCENARIOS
from simulation import Simulation


OUTPUT_DIR = "output"


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_all_scenarios() -> pd.DataFrame:
    frames = []

    for i, scenario in enumerate(SCENARIOS):
        print(f"Rodando cenário: {scenario.name}")
        sim = Simulation(scenario=scenario, years=20, seed=100 + i)
        df = sim.run()
        frames.append(df)

    results = pd.concat(frames, ignore_index=True)
    return results


def save_results(results: pd.DataFrame):
    results.to_csv(os.path.join(OUTPUT_DIR, "simulation_results.csv"), index=False)

    final_year = results["year"].max()
    comparison = (
        results[results["year"] == final_year][
            [
                "scenario",
                "avg_knowledge",
                "avg_computational",
                "pisa_like",
                "tech_ready_share",
                "economy_productivity",
                "capital_attraction",
                "innovation_capacity",
                "education_investment",
                "effective_spending",
                "spending_loss",
                "institutional_quality",
            ]
        ]
        .sort_values("pisa_like", ascending=False)
        .reset_index(drop=True)
    )

    comparison.to_csv(os.path.join(OUTPUT_DIR, "comparison_final_year.csv"), index=False)
    print("\nComparação final:")
    print(comparison)

    return comparison


def plot_metric(results: pd.DataFrame, metric: str, title: str, ylabel: str, filename: str):
    plt.figure(figsize=(10, 6))

    for scenario_name, group in results.groupby("scenario"):
        plt.plot(group["year"], group[metric], label=scenario_name)

    plt.title(title)
    plt.xlabel("Ano")
    plt.ylabel(ylabel)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=180)
    plt.close()


def generate_plots(results: pd.DataFrame, comparison: pd.DataFrame):
    plot_metric(
        results,
        metric="pisa_like",
        title="Desempenho educacional sintético ao longo do tempo",
        ylabel="Indicador tipo PISA",
        filename="grafico_pisa_like.png",
    )

    plot_metric(
        results,
        metric="avg_computational",
        title="Evolução do pensamento computacional",
        ylabel="Média",
        filename="grafico_pensamento_computacional.png",
    )

    plot_metric(
        results,
        metric="economy_productivity",
        title="Produtividade econômica ao longo do tempo",
        ylabel="Produtividade",
        filename="grafico_produtividade.png",
    )

    plot_metric(
        results,
        metric="capital_attraction",
        title="Atração de capital ao longo do tempo",
        ylabel="Índice",
        filename="grafico_atracao_capital.png",
    )

    plot_metric(
        results,
        metric="innovation_capacity",
        title="Capacidade de inovação ao longo do tempo",
        ylabel="Índice",
        filename="grafico_inovacao.png",
    )

    plot_metric(
        results,
        metric="effective_spending",
        title="Gasto educacional efetivo ao longo do tempo",
        ylabel="Gasto efetivo",
        filename="grafico_gasto_efetivo.png",
    )

    plot_metric(
        results,
        metric="tech_ready_share",
        title="Proporção de alunos prontos para áreas tecnológicas",
        ylabel="Proporção",
        filename="grafico_prontos_tecnologia.png",
    )

    plot_metric(
        results,
        metric="inequality_cv",
        title="Desigualdade educacional relativa",
        ylabel="Coeficiente de variação",
        filename="grafico_desigualdade.png",
    )

    plt.figure(figsize=(10, 6))
    plt.barh(comparison["scenario"], comparison["pisa_like"])
    plt.title("Comparação final dos cenários — indicador educacional tipo PISA")
    plt.xlabel("Pontuação")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "grafico_barra_comparacao_pisa.png"), dpi=180)
    plt.close()


def save_summary(comparison: pd.DataFrame):
    baseline = comparison[comparison["scenario"] == "Baseline_sem_computacao"].iloc[0]
    virtuoso = comparison[comparison["scenario"] == "Ciclo_virtuoso_completo"].iloc[0]
    estruturada = comparison[comparison["scenario"] == "Computacao_estruturada"].iloc[0]
    mau_ambiente = comparison[comparison["scenario"] == "Boa_educacao_mau_ambiente_institucional"].iloc[0]
    pouca_eficiencia = comparison[comparison["scenario"] == "Muito_gasto_pouca_eficiencia"].iloc[0]

    def pct_change(base, value):
        return (value / base - 1.0) * 100.0

    summary = f"""
Resumo analítico da simulação

1. Melhor resultado geral:
- cenário: Ciclo_virtuoso_completo
- indicador tipo PISA final: {virtuoso['pisa_like']:.1f}
- ganho sobre baseline: {pct_change(baseline['pisa_like'], virtuoso['pisa_like']):.1f}%

2. Computação estruturada:
- indicador tipo PISA final: {estruturada['pisa_like']:.1f}
- ganho sobre baseline: {pct_change(baseline['pisa_like'], estruturada['pisa_like']):.1f}%

3. Boa educação com mau ambiente institucional:
- indicador tipo PISA final: {mau_ambiente['pisa_like']:.1f}
- diferença para computação estruturada: {estruturada['pisa_like'] - mau_ambiente['pisa_like']:.1f} pontos

4. Muito gasto e pouca eficiência:
- investimento educacional nominal final: {pouca_eficiencia['education_investment']:.2f}
- gasto efetivo final: {pouca_eficiencia['effective_spending']:.2f}
- perda estimada: {pouca_eficiencia['spending_loss']:.2f}

5. Leitura geral:
O modelo sugere que o ensino de computação melhora os resultados educacionais e tecnológicos,
mas sua conversão em produtividade e atração de capital depende fortemente da qualidade institucional.
"""

    with open(os.path.join(OUTPUT_DIR, "resumo_analitico.txt"), "w", encoding="utf-8") as file:
        file.write(summary.strip())


def main():
    ensure_output_dir()
    results = run_all_scenarios()
    comparison = save_results(results)
    generate_plots(results, comparison)
    save_summary(comparison)

    print("\nArquivos gerados em ./output")
    print("- simulation_results.csv")
    print("- comparison_final_year.csv")
    print("- resumo_analitico.txt")
    print("- gráficos PNG")


if __name__ == "__main__":
    main()

