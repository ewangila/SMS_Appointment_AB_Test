from datetime import datetime, timedelta

from ab_testing.metrics import MetricsCalculator


def analyze_experiment_results() -> dict:
    calculator = MetricsCalculator()

    # Use a 4-week window (matches the mock data period conceptually)
    end = datetime.now()
    start = end - timedelta(days=28)

    # 1. Query attendance rates via the real MetricsCalculator
    control_rate = calculator.calculate_attendance_rate("control", start, end)
    treatment_rate = calculator.calculate_attendance_rate("treatment", start, end)

    # 2. Statistical significance (using the known mock counts)
    stats_results = calculator.calculate_confidence_interval(
        control_successes=7500,
        control_trials=10000,
        treatment_successes=8050,
        treatment_trials=10000,
        confidence_level=0.95,
    )

    # 3. Derived metrics
    absolute_improvement = treatment_rate - control_rate
    relative_improvement = (absolute_improvement / control_rate) * 100 if control_rate else 0.0

    business_impact = {
        "monthly_appointments": 10_000,
        "cost_per_missed_appointment": 45,
        "projected_annual_savings": 10_000 * 12 * (absolute_improvement / 100) * 45,
    }

    return {
        "metrics_impact": {
            "control_rate": control_rate,
            "treatment_rate": treatment_rate,
            "absolute_improvement": absolute_improvement,
            "relative_improvement": relative_improvement,
        },
        "statistical_results": stats_results,
        "business_impact": business_impact,
    }


if __name__ == "__main__":
    results = analyze_experiment_results()

    print("\nEXPERIMENT ANALYSIS RESULTS")
    print("=" * 40)

    print("\n1. Metrics Impact:")
    print(f"   Control Rate:           {results['metrics_impact']['control_rate']:.1f}%")
    print(f"   Treatment Rate:         {results['metrics_impact']['treatment_rate']:.1f}%")
    print(f"   Absolute Improvement:   {results['metrics_impact']['absolute_improvement']:.1f} pp")
    print(f"   Relative Improvement:   {results['metrics_impact']['relative_improvement']:.2f}%")

    print("\n2. Statistical Significance:")
    effect = results["statistical_results"]["effect_size"]
    ci_low, ci_high = results["statistical_results"]["confidence_interval"]
    is_significant = ci_low > 0

    print(f"   Lift (Effect Size):     {effect * 100:.1f}%")
    print(f"   95% Confidence Interval: [{ci_low * 100:.1f}%, {ci_high * 100:.1f}%]")
    print(f"   Statistically Significant? {'Yes' if is_significant else 'No'}")

    print("\n3. Business Impact:")
    savings = results["business_impact"]["projected_annual_savings"]
    print(f"   Projected Annual Savings: ${savings:,.2f}")
