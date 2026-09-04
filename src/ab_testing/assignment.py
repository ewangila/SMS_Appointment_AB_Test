import hashlib
from datetime import datetime
from typing import Dict

class NotificationSystem:
    def send_email(self, user_id, template, appointment_details):
        print(f"📧 Email sent to User {user_id} for appointment {appointment_details['appointment_id']}")
        
    def send_sms(self, user_id, template, appointment_details):
        print(f"📱 SMS sent to User {user_id} for appointment {appointment_details['appointment_id']}")

#  The Core Experiment Class
class Experiment:
    def __init__(self, experiment_id: str, traffic_percentage: float = 0.5):
        self.experiment_id = experiment_id
        self.traffic_percentage = traffic_percentage
        self.start_time = datetime.now()
        
    def get_variant(self, user_id: str) -> str:
        """Deterministically assign users to variants using hashing"""
        hash_input = f"{user_id}:{self.experiment_id}".encode('utf-8')
        hash_value = int(hashlib.sha256(hash_input).hexdigest(), 16)
        
        # Check if user falls into the traffic allocation (e.g., 50%)
        is_in_experiment = (hash_value % 100) < (self.traffic_percentage * 100)
        if not is_in_experiment:
            return 'excluded'
            
        return 'treatment' if (hash_value % 2) == 0 else 'control'
        
    def is_eligible(self, user: Dict) -> bool:
        """Determine if a user is eligible for the experiment"""
        return (
            user.get('has_phone_number', False) and  
            user.get('communication_preferences', {}).get('sms_enabled', False) and  
            user.get('appointment_count', 0) > 0  
        )

#  The Specific Reminder Experiment
class ReminderExperiment(Experiment):
    def __init__(self):
        super().__init__('reminder_optimization_2024Q1')
        self.notification_system = NotificationSystem()
        
    def send_reminders(self, appointment: Dict) -> None:
        user_id = appointment['user_id']
        variant = self.get_variant(user_id)
        
        print(f"\nProcessing User {user_id} -> Assigned to: {variant.upper()}")
        
        # Both groups get email
        self.notification_system.send_email(
            user_id=user_id,
            template='appointment_reminder',
            appointment_details=appointment
        )
        
        # Treatment group also gets SMS
        if variant == 'treatment':
            self.notification_system.send_sms(
                user_id=user_id,
                template='appointment_reminder_sms',
                appointment_details=appointment
            )

# Test the implementation 
if __name__ == "__main__":
    experiment = ReminderExperiment()
    
    # Simulate some appointments
    test_appointments = [
        {"user_id": "user_101", "appointment_id": "A-001"},
        {"user_id": "user_102", "appointment_id": "A-002"},
        {"user_id": "user_103", "appointment_id": "A-003"}
    ]
    
    for appt in test_appointments:
        experiment.send_reminders(appt)
