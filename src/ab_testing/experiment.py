# experiment.py

experiment_definition = {
    "business_question": "Will SMS reminders increase appointment attendance?",
    "null_hypothesis": "Adding SMS reminders has no effect on appointment attendance rates",
    "alternative_hypothesis": "Adding SMS reminders increases appointment attendance rates",
    "minimum_detectable_effect": 0.05,  # 5% improvement needed to justify SMS costs
    "primary_metric": "appointment_attendance_rate",
    "secondary_metrics": [
        "patient_satisfaction_score",
        "provider_satisfaction_score",
        "support_contact_rate"
    ],
    "guardrail_metrics": [
        "app_crash_rate",
        "system_error_rate"
    ]
}

print("Experiment definition loaded successfully.")