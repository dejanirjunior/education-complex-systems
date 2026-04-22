import os
from dataclasses import asdict
from time import time

import pandas as pd
from flask import Flask, render_template, request, send_file

from scenarios import Scenario, SCENARIOS
from simulation import Simulation

from werkzeug.middleware.proxy_fix import ProxyFix

APP_PASSWORD = os.environ.get("APP_PASSWORD", "simulador2026")

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_prefix=1)

STATIC_OUTPUT_DIR = os.path.join("static", "output")
os.makedirs(STATIC_OUTPUT_DIR, exist_ok=True)

DEFAULT_SCENARIO_NAME = "Computacao_estruturada"
LAST_RUN = 0


SCENARIO_DESCRIPTIONS = {
    "Baseline_sem_computacao": "Cenário de referência, sem política estruturada de ensino de computação.",
    "Computacao_superficial": "Há computação no sistema, mas com implementação parcial e menor profundidade.",
    "Computacao_estruturada": "A computação é inserida de forma consistente, com melhores condições pedagógicas e institucionais.",
    "Boa_educacao_mau_ambiente_institucional": "A educação melhora, mas o ambiente institucional reduz a conversão em inovação e produtividade.",
    "Ciclo_virtuoso_completo": "Combina ensino de computação estruturado, boa governança, maior liberdade econômica e incentivo à inovação.",
    "Muito_gasto_pouca_eficiencia": "Representa situações em que o investimento nominal é alto, mas a eficiência de conversão em resultado é baixa.",
}


def get_scenario_by_name(name: str) -> Scenario:
    for scenario in SCENARIOS:
        if scenario.name == name:
            return scenario
    return SCENARIOS[0]


def plot_multi_metric(results: pd.DataFrame, metric: str, title: str, ylabel: str, filename: str):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    for scenario_name, group in results.groupby("scenario"):
        plt.plot(group["year"], group[metric], label=scenario_name)

    plt.title(title)
    plt.xlabel("Ano")
    plt.ylabel(ylabel)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_OUTPUT_DIR, filename), dpi=180)
    plt.close()


def plot_single_metric(results: pd.DataFrame, metric: str, title: str, ylabel: str, filename: str):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    plt.plot(results["year"], results[metric])
    plt.title(title)
    plt.xlabel("Ano")
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_OUTPUT_DIR, filename), dpi=180)
    plt.close()


def run_default_comparison():
    frames = []

    for i, scenario in enumerate(SCENARIOS):
        sim = Simulation(
            scenario=scenario,
            n_students=1200,
            n_teachers=60,
            n_schools=30,
            n_companies=80,
            years=20,
            seed=100 + i,
        )
        frames.append(sim.run())

    results = pd.concat(frames, ignore_index=True)

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

    plot_multi_metric(results, "pisa_like", "Comparação padrão — desempenho educacional sintético", "Indicador tipo PISA", "default_grafico_pisa_like.png")
    plot_multi_metric(results, "avg_computational", "Comparação padrão — pensamento computacional", "Média", "default_grafico_pensamento_computacional.png")
    plot_multi_metric(results, "economy_productivity", "Comparação padrão — produtividade econômica", "Produtividade", "default_grafico_produtividade.png")
    plot_multi_metric(results, "capital_attraction", "Comparação padrão — atração de capital", "Índice", "default_grafico_atracao_capital.png")
    plot_multi_metric(results, "innovation_capacity", "Comparação padrão — capacidade de inovação", "Índice", "default_grafico_inovacao.png")
    plot_multi_metric(results, "effective_spending", "Comparação padrão — gasto educacional efetivo", "Gasto", "default_grafico_gasto_efetivo.png")
    plot_multi_metric(results, "tech_ready_share", "Comparação padrão — alunos prontos para áreas tecnológicas", "Proporção", "default_grafico_prontos_tecnologia.png")
    plot_multi_metric(results, "inequality_cv", "Comparação padrão — desigualdade educacional relativa", "Coeficiente de variação", "default_grafico_desigualdade.png")

    return results, comparison


def generate_default_insights(comparison: pd.DataFrame):
    insights = []

    baseline = comparison[comparison["scenario"] == "Baseline_sem_computacao"].iloc[0]
    best = comparison.iloc[0]
    structured = comparison[comparison["scenario"] == "Computacao_estruturada"].iloc[0]
    bad_env = comparison[comparison["scenario"] == "Boa_educacao_mau_ambiente_institucional"].iloc[0]
    waste = comparison[comparison["scenario"] == "Muito_gasto_pouca_eficiencia"].iloc[0]

    gain_best = ((best["pisa_like"] / baseline["pisa_like"]) - 1) * 100
    gain_structured = ((structured["pisa_like"] / baseline["pisa_like"]) - 1) * 100
    diff_structured_bad = structured["pisa_like"] - bad_env["pisa_like"]

    insights.append(
        f"O melhor resultado padrão foi {best['scenario']}, superando o baseline em {gain_best:.1f}% no indicador educacional sintético."
    )
    insights.append(
        f"O cenário Computacao_estruturada superou o baseline em {gain_structured:.1f}%, sugerindo ganho relevante com inserção consistente do ensino de computação."
    )
    insights.append(
        f"A diferença de {diff_structured_bad:.1f} pontos entre Computacao_estruturada e Boa_educacao_mau_ambiente_institucional mostra que a qualidade institucional modula fortemente os resultados."
    )
    insights.append(
        f"No cenário Muito_gasto_pouca_eficiencia, a perda estimada entre gasto nominal e gasto efetivo foi de {waste['spending_loss']:.2f}, reforçando que gasto bruto não equivale automaticamente a resultado."
    )

    return insights


def run_custom_simulation(
    scenario: Scenario,
    n_students: int,
    n_teachers: int,
    n_schools: int,
    n_companies: int,
    years: int,
    seed: int,
):
    sim = Simulation(
        scenario=scenario,
        n_students=n_students,
        n_teachers=n_teachers,
        n_schools=n_schools,
        n_companies=n_companies,
        years=years,
        seed=seed,
    )

    df = sim.run()
    final_row = df[df["year"] == df["year"].max()].iloc[0]

    summary_df = pd.DataFrame([final_row[[
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
    ]]]).round(4)

    plot_single_metric(df, "pisa_like", "Experimento — desempenho educacional sintético", "Indicador tipo PISA", "custom_grafico_pisa_like.png")
    plot_single_metric(df, "avg_computational", "Experimento — pensamento computacional", "Média", "custom_grafico_pensamento_computacional.png")
    plot_single_metric(df, "economy_productivity", "Experimento — produtividade econômica", "Produtividade", "custom_grafico_produtividade.png")
    plot_single_metric(df, "capital_attraction", "Experimento — atração de capital", "Índice", "custom_grafico_atracao_capital.png")
    plot_single_metric(df, "innovation_capacity", "Experimento — capacidade de inovação", "Índice", "custom_grafico_inovacao.png")
    plot_single_metric(df, "effective_spending", "Experimento — gasto educacional efetivo", "Gasto", "custom_grafico_gasto_efetivo.png")
    plot_single_metric(df, "tech_ready_share", "Experimento — alunos prontos para áreas tecnológicas", "Proporção", "custom_grafico_prontos_tecnologia.png")
    plot_single_metric(df, "inequality_cv", "Experimento — desigualdade educacional relativa", "Coeficiente de variação", "custom_grafico_desigualdade.png")

    custom_charts = [
        ("custom_grafico_pisa_like.png", "Mostra a evolução do desempenho educacional sintético na rodada personalizada."),
        ("custom_grafico_pensamento_computacional.png", "Mostra a evolução do pensamento computacional na rodada personalizada."),
        ("custom_grafico_produtividade.png", "Mostra a trajetória da produtividade econômica na rodada personalizada."),
        ("custom_grafico_atracao_capital.png", "Mostra a evolução da atração de capital na rodada personalizada."),
        ("custom_grafico_inovacao.png", "Mostra a evolução da capacidade de inovação na rodada personalizada."),
        ("custom_grafico_gasto_efetivo.png", "Mostra quanto do investimento foi efetivamente convertido em ação útil."),
        ("custom_grafico_prontos_tecnologia.png", "Mostra a evolução da base de alunos mais aderente a trajetórias tecnológicas."),
        ("custom_grafico_desigualdade.png", "Mostra como a desigualdade educacional se comportou ao longo da rodada."),
    ]

    used_params = {
        "scenario": asdict(scenario),
        "n_students": n_students,
        "n_teachers": n_teachers,
        "n_schools": n_schools,
        "n_companies": n_companies,
        "years": years,
        "seed": seed,
    }

    custom_csv_path = os.path.join(STATIC_OUTPUT_DIR, "custom_simulation_results.csv")
    df.to_csv(custom_csv_path, index=False)

    return summary_df, final_row, custom_charts, used_params, custom_csv_path


def generate_custom_insights(final_row: pd.Series):
    insights = []

    if final_row["avg_computational"] > 1.5:
        insights.append("O experimento produziu crescimento relevante do pensamento computacional.")
    if final_row["economy_productivity"] > 2.0:
        insights.append("A produtividade econômica final ficou elevada, indicando boa conversão de capital humano em resultado agregado.")
    if final_row["spending_loss"] > 0.5:
        insights.append("A perda entre gasto nominal e gasto efetivo foi significativa.")
    if final_row["institutional_quality"] < 0.5:
        insights.append("A qualidade institucional final permaneceu baixa, limitando os efeitos da política.")
    if final_row["tech_ready_share"] > 0.4:
        insights.append("A proporção de alunos prontos para áreas tecnológicas ficou alta.")
    if not insights:
        insights.append("O experimento gerou avanços moderados, sem aceleração forte nas variáveis centrais.")

    return insights


@app.route("/download/custom-csv")
def download_custom_csv():
    file_path = os.path.join(STATIC_OUTPUT_DIR, "custom_simulation_results.csv")
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "Arquivo CSV da rodada personalizada não encontrado.", 404


@app.route("/custom-report")
def custom_report():
    file_path = os.path.join(STATIC_OUTPUT_DIR, "custom_simulation_results.csv")
    if not os.path.exists(file_path):
        return "Nenhuma rodada personalizada encontrada.", 404

    df = pd.read_csv(file_path)
    final_row = df[df["year"] == df["year"].max()].iloc[0]

    summary_df = pd.DataFrame([final_row[[
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
    ]]]).round(4)

    summary_html = summary_df.to_html(index=False, border=0, classes="comparison-table")
    insights = generate_custom_insights(final_row)

    return render_template(
        "custom_report.html",
        summary_html=summary_html,
        insights=insights,
    )


@app.route("/", methods=["GET", "POST"])
def index():
    global LAST_RUN

    default_results, default_comparison = run_default_comparison()
    default_insights = generate_default_insights(default_comparison)

    default_comparison_html = default_comparison.to_html(index=False, classes="comparison-table", border=0)

    default_chart_files = [
        ("default_grafico_pisa_like.png", "Comparação padrão do desempenho educacional sintético."),
        ("default_grafico_pensamento_computacional.png", "Comparação padrão do pensamento computacional."),
        ("default_grafico_produtividade.png", "Comparação padrão da produtividade econômica."),
        ("default_grafico_atracao_capital.png", "Comparação padrão da atração de capital."),
        ("default_grafico_inovacao.png", "Comparação padrão da capacidade de inovação."),
        ("default_grafico_gasto_efetivo.png", "Comparação padrão do gasto educacional efetivo."),
        ("default_grafico_prontos_tecnologia.png", "Comparação padrão da base de alunos prontos para áreas tecnológicas."),
        ("default_grafico_desigualdade.png", "Comparação padrão da desigualdade educacional relativa."),
    ]

    selected_base = get_scenario_by_name(DEFAULT_SCENARIO_NAME)
    custom_results_html = None
    custom_insights = []
    custom_chart_files = []
    used_params = None
    has_custom = False
    form_data = None
    success_message = None
    error_message = None

    if request.method == "POST" and request.form.get("action") == "run_custom":
        form_data = request.form.to_dict()

        base_name = request.form.get("base_scenario", DEFAULT_SCENARIO_NAME)
        base = get_scenario_by_name(base_name)
        selected_base = base

        password = request.form.get("password", "")

        if password != APP_PASSWORD:
            error_message = "Acesso restrito. Senha incorreta. Os parâmetros preenchidos foram mantidos para você tentar novamente."
            return render_template(
                "index.html",
                scenario_descriptions=SCENARIO_DESCRIPTIONS,
                scenarios=SCENARIOS,
                selected_base=selected_base,
                default_comparison_html=default_comparison_html,
                default_insights=default_insights,
                default_chart_files=default_chart_files,
                custom_results_html=custom_results_html,
                custom_insights=custom_insights,
                custom_chart_files=custom_chart_files,
                used_params=used_params,
                has_custom=has_custom,
                form_data=form_data,
                error_message=error_message,
                success_message=success_message,
            )

        if time() - LAST_RUN < 10:
            error_message = "Aguarde alguns segundos antes de rodar nova simulação."
            return render_template(
                "index.html",
                scenario_descriptions=SCENARIO_DESCRIPTIONS,
                scenarios=SCENARIOS,
                selected_base=selected_base,
                default_comparison_html=default_comparison_html,
                default_insights=default_insights,
                default_chart_files=default_chart_files,
                custom_results_html=custom_results_html,
                custom_insights=custom_insights,
                custom_chart_files=custom_chart_files,
                used_params=used_params,
                has_custom=has_custom,
                form_data=form_data,
                error_message=error_message,
                success_message=success_message,
            )

        LAST_RUN = time()

        scenario = Scenario(
            name=request.form.get("custom_name", "Cenario_personalizado"),
            education_investment=float(request.form.get("education_investment", base.education_investment)),
            computation_policy=float(request.form.get("computation_policy", base.computation_policy)),
            efficiency=float(request.form.get("efficiency", base.efficiency)),
            corruption=float(request.form.get("corruption", base.corruption)),
            risk=float(request.form.get("risk", base.risk)),
            economic_freedom=float(request.form.get("economic_freedom", base.economic_freedom)),
            innovation_incentive=float(request.form.get("innovation_incentive", base.innovation_incentive)),
            policy_stability=float(request.form.get("policy_stability", base.policy_stability)),
            teacher_training=float(request.form.get("teacher_training", base.teacher_training)),
            accountability=float(request.form.get("accountability", base.accountability)),
            financial_recognition=float(request.form.get("financial_recognition", base.financial_recognition)),
            state_policy=float(request.form.get("state_policy", base.state_policy)),
            family_support_mean=float(request.form.get("family_support_mean", base.family_support_mean)),
            school_management=float(request.form.get("school_management", base.school_management)),
            bureaucracy=float(request.form.get("bureaucracy", base.bureaucracy)),
        )

        n_students = min(int(request.form.get("n_students", 1200)), 5000)
        n_teachers = min(int(request.form.get("n_teachers", 60)), 500)
        n_schools = min(int(request.form.get("n_schools", 30)), 200)
        n_companies = min(int(request.form.get("n_companies", 80)), 5000)
        years = min(int(request.form.get("years", 20)), 50)
        seed = int(request.form.get("seed", 42))

        summary_df, final_row, custom_chart_files, used_params, custom_csv_path = run_custom_simulation(
            scenario=scenario,
            n_students=n_students,
            n_teachers=n_teachers,
            n_schools=n_schools,
            n_companies=n_companies,
            years=years,
            seed=seed,
        )

        custom_results_html = summary_df.to_html(index=False, classes="comparison-table", border=0)
        custom_insights = generate_custom_insights(final_row)
        has_custom = True
        success_message = "Simulação executada com sucesso."

    return render_template(
        "index.html",
        scenario_descriptions=SCENARIO_DESCRIPTIONS,
        scenarios=SCENARIOS,
        selected_base=selected_base,
        default_comparison_html=default_comparison_html,
        default_insights=default_insights,
        default_chart_files=default_chart_files,
        custom_results_html=custom_results_html,
        custom_insights=custom_insights,
        custom_chart_files=custom_chart_files,
        used_params=used_params,
        has_custom=has_custom,
        form_data=form_data,
        error_message=error_message,
        success_message=success_message,
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


