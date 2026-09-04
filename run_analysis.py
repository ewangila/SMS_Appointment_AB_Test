from statsmodels.stats.proportion import confint_proportions_2indep

class MetricsCalculator:
    def get_metrics(self, variant: str):
        """Simulate fetching 4 weeks of data from the database."""
        if variant == 'control':
            return {'attended': 7500, 'total': 10000, 'attendance_rate': 0.75}
        else:
            # Treatment performed better (80.5% vs 75%)
            return {'attended': 8050, 'total': 10000, 'attendance_rate': 0.805}

    def calculate_confidence_interval(self, control_successes, control_trials, treatment_successes, treatment_trials):
        """Calculate confidence interval for difference in proportions."""
        p_control = control_successes / control_trials
        p_treatment = treatment_successes / treatment_trials
        effect_size = p_treatment - p_control
        
        ci_low, ci_high = confint_proportions_2indep(
            count1=treatment_successes, nobs1=treatment_trials,
            count2=control_successes, nobs2=control_trials,
            compare='diff',
            alpha=0.05
        )
        return {'effect_size': effect_size, 'confidence_interval': (ci_low, ci_high)}

def analyze_experiment_results():
    calculator = MetricsCalculator()
    
    # Get results for both variants
    control_metrics = calculator.get_metrics('control')
    treatment_metrics = calculator.get_metrics('treatment')
    
    # Calculate primary metric impact
    attendance_impact = {
        'control_rate': control_metrics['attendance_rate'],
        'treatment_rate': treatment_metrics['attendance_rate'],
        'absolute_improvement': (
            treatment_metrics['attendance_rate'] - 
            control_metrics['attendance_rate']
        ),
        'relative_improvement': (
            (treatment_metrics['attendance_rate'] - 
             control_metrics['attendance_rate']) / 
            control_metrics['attendance_rate'] * 100
        )
    }
    
    # Calculate statistical significance
    stats_results = calculator.calculate_confidence_interval(
        control_metrics['attended'],
        control_metrics['total'],
        treatment_metrics['attended'],
        treatment_metrics['total']
    )
    
    # Calculate business impact
    business_impact = {
        'monthly_appointments': 10000,  
        'cost_per_missed_appointment': 45,  
        'projected_annual_savings': (
            10000 * 12 * attendance_impact['absolute_improvement'] * 45
        )
    }
    
    return {
        'metrics_impact': attendance_impact,
        'statistical_results': stats_results,
        'business_impact': business_impact
    }

if __name__ == "__main__":
    # Run the analysis
    results = analyze_experiment_results()
    
    # Display the results
    print("\nEXPERIMENT ANALYSIS RESULTS ")
    
    print("\n1. Metrics Impact:")
    print(f"   Control Rate: {results['metrics_impact']['control_rate']:.1%}")
    print(f"   Treatment Rate: {results['metrics_impact']['treatment_rate']:.1%}")
    print(f"   Absolute Improvement: {results['metrics_impact']['absolute_improvement']:.1%}")
    print(f"   Relative Improvement: {results['metrics_impact']['relative_improvement']:.2f}%")
    
    print("\n2. Statistical Significance:")
    ci_low = results['statistical_results']['confidence_interval'][0]
    ci_high = results['statistical_results']['confidence_interval'][1]
    is_significant = ci_low > 0
    
    print(f"   Lift (Effect Size): {results['statistical_results']['effect_size']:.1%}")
    print(f"   95% Confidence Interval: [{ci_low:.1%}, {ci_high:.1%}]")
    print(f"   Statistically Significant? {' Yes' if is_significant else '❌ No'}")
    
    print("\n3. Business Impact:")
    savings = results['business_impact']['projected_annual_savings']
    print(f"   Projected Annual Savings: ${savings:,.2f}")