from typing import Dict

def generate_experiment_report(results: Dict) -> str:
    """Generate a comprehensive experiment report"""
    
    report = f"""
    A/B Test Results: Appointment Reminder Optimization
    

    Experiment Overview:
    - Duration: 4 weeks
    - Total Participants: {results['control_size'] + results['treatment_size']:,}
    - Control Group Size: {results['control_size']:,}
    - Treatment Group Size: {results['treatment_size']:,}

    Results:
    - Control Attendance Rate: {results['metrics_impact']['control_rate']:.1f}%
    - Treatment Attendance Rate: {results['metrics_impact']['treatment_rate']:.1f}%
    - Absolute Improvement: {results['metrics_impact']['absolute_improvement']:.1f} percentage points
    - Relative Improvement: {results['metrics_impact']['relative_improvement']:.1f}%

    Statistical Significance:
    - P-value: {results['statistical_results']['p_value']:.4f}
    - Confidence Interval: ({results['statistical_results']['confidence_interval'][0]:.1f}%, {results['statistical_results']['confidence_interval'][1]:.1f}%)

    Business Impact:
    - Projected Annual Savings: ${results['business_impact']['projected_annual_savings']:,.2f}
    - Implementation Cost (SMS): ${results['business_impact']['sms_cost']:,.2f}
    - Net Annual Impact: ${results['business_impact']['net_impact']:,.2f}

    Recommendation:
    Based on the {results['metrics_impact']['absolute_improvement']:.1f} percentage point 
    improvement in attendance rates and projected annual savings of 
    ${results['business_impact']['net_impact']:,.2f}, we recommend implementing 
    SMS reminders for all appointments.

    Next Steps:
    1. Gradually roll out SMS reminders to all users over 4 weeks
    2. Monitor system performance and costs during rollout
    3. Conduct follow-up analysis after full rollout to verify results at scale
    """
    return report

if __name__ == "__main__":
    # We construct the final 'results' dictionary combining our data from Step 4
    # and adding the new business/statistical fields needed for the report.
    
    # SMS Cost Calculation: 
    # 10,000 monthly appointments * 12 months = 120,000 per year
    # $0.05 per SMS
    annual_sms_cost = 120000 * 0.05
    annual_savings = 10000 * 12 * 0.055 * 45  # (Appointments * 12 * 5.5% lift * $45)
    
    final_results = {
        'control_size': 10000,
        'treatment_size': 10000,
        'metrics_impact': {
            'control_rate': 75.0,          # Passed as percentages to match the f-string formatting
            'treatment_rate': 80.5,
            'absolute_improvement': 5.5, 
            'relative_improvement': 7.33   # (80.5 - 75.0) / 75.0 * 100
        },
        'statistical_results': {
            'p_value': 0.0001,             # A very low P-value means high confidence
            'confidence_interval': (4.8, 6.2)
        },
        'business_impact': {
            'projected_annual_savings': annual_savings,
            'sms_cost': annual_sms_cost,
            'net_impact': annual_savings - annual_sms_cost
        }
    }
    
    # Generate and print the report
    final_report = generate_experiment_report(final_results)
    print(final_report)