import sqlite3
from datetime import datetime, timedelta
from typing import Dict
from statsmodels.stats.proportion import confint_proportions_2indep

class DatabaseConnection:
    """Mock database connection running SQLite in-memory."""
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self._populate_mock_data()

    def _populate_mock_data(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE appointments (
                appointment_id TEXT,
                user_id TEXT,
                variant TEXT,
                attended INTEGER,
                appointment_time TIMESTAMP
            )
        """)
        
        now = datetime.now()
        data = []
        
        # Simulate Control Group: 10,000 appointments, ~7,500 attended (75.0%)
        for i in range(10000):
            data.append((f"A_C_{i}", f"U_{i}", "control", 1 if i < 7500 else 0, now))
            
        # Simulate Treatment Group: 10,000 appointments, ~8,050 attended (80.5%)
        for i in range(10000):
            data.append((f"A_T_{i}", f"U_{10000+i}", "treatment", 1 if i < 8050 else 0, now))

        cursor.executemany("INSERT INTO appointments VALUES (?, ?, ?, ?, ?)", data)
        self.conn.commit()

    def execute_query(self, query: str, params: Dict) -> float:
        cursor = self.conn.cursor()
        # Convert PostgreSQL/MySQL named placeholders %(var)s to SQLite style :var
        sqlite_query = query.replace("%(", ":").replace(")s", "")
        cursor.execute(sqlite_query, params)
        result = cursor.fetchone()
        return result[0] if result and result[0] is not None else 0.0

class MetricsCalculator:
    def __init__(self):
        self.db = DatabaseConnection()
        
    def calculate_attendance_rate(self, variant: str, 
                                  start_date: datetime, 
                                  end_date: datetime) -> float:
        """Calculate attendance rate for a variant using SQL."""
        query = """
        SELECT 
            COUNT(CASE WHEN attended = 1 THEN 1 END) * 100.0 / COUNT(*) as attendance_rate
        FROM appointments
        WHERE variant = %(variant)s
            AND appointment_time BETWEEN %(start_date)s AND %(end_date)s
        """
        return self.db.execute_query(query, {
            'variant': variant,
            'start_date': start_date,
            'end_date': end_date
        })
        
    def calculate_confidence_interval(self, 
                                     control_successes: int, 
                                     control_trials: int,
                                     treatment_successes: int, 
                                     treatment_trials: int,
                                     confidence_level: float = 0.95) -> Dict:
        """Calculate confidence interval for the difference in proportions."""
        
        # Calculate effect size (Absolute Difference)
        p_control = control_successes / control_trials
        p_treatment = treatment_successes / treatment_trials
        effect_size = p_treatment - p_control
        
        # Confidence interval for difference between 2 independent proportions
        ci_low, ci_high = confint_proportions_2indep(
            count1=treatment_successes, nobs1=treatment_trials,
            count2=control_successes, nobs2=control_trials,
            compare='diff',
            alpha=(1 - confidence_level)
        )
        
        return {
            'effect_size': effect_size,
            'confidence_interval': (ci_low, ci_high)
        }

# --- Execution Test ---
if __name__ == "__main__":
    calculator = MetricsCalculator()
    
    start_time = datetime.now() - timedelta(days=1)
    end_time = datetime.now() + timedelta(days=1)
    
    # 1. Query attendance rates via SQL
    control_rate = calculator.calculate_attendance_rate('control', start_time, end_time)
    treatment_rate = calculator.calculate_attendance_rate('treatment', start_time, end_time)
    
    print(f"Control Attendance Rate: {control_rate:.2f}%")
    print(f"Treatment Attendance Rate: {treatment_rate:.2f}%")
    
    # 2. Compute 95% Confidence Interval on difference
    ci_results = calculator.calculate_confidence_interval(
        control_successes=7500, control_trials=10000,
        treatment_successes=8050, treatment_trials=10000
    )
    
    print(f"\nAbsolute Lift (Effect Size): {ci_results['effect_size'] * 100:.2f}%")
    print(f"95% Confidence Interval for Lift: [{ci_results['confidence_interval'][0]*100:.2f}%, {ci_results['confidence_interval'][1]*100:.2f}%]")