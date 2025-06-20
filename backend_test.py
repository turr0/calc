import requests
import json
import unittest
import os
import math

# Get the backend URL from environment variable
BACKEND_URL = "https://0b90ee0f-4a97-4e5c-a6f0-d0c248483af7.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

class TestROICalculatorAPI(unittest.TestCase):
    
    def test_health_check(self):
        """Test the /api/health endpoint to ensure the API is running"""
        response = requests.get(f"{API_BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["message"], "ROI Calculator API is running")
        print("✅ Health check API test passed")
    
    def test_basic_roi_calculation(self):
        """Test /api/calculate-roi with default Argentine SME values"""
        payload = {
            "monthly_inquiries": 1000,
            "automation_percentage": 60,
            "minutes_per_inquiry": 4,
            "monthly_crm_hours": 40,
            "crm_automation_percentage": 50,
            "team_members": 3,
            "hourly_cost_ars": 5000,
            "bitrix24_annual_cost": 200000,
            "implementation_cost": 1000000
        }
        
        response = requests.post(f"{API_BASE_URL}/calculate-roi", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify all required fields are present
        self.assertIn("inputs", data)
        self.assertIn("chatbot_monthly_hours_saved", data)
        self.assertIn("chatbot_annual_savings", data)
        self.assertIn("crm_annual_hours_saved", data)
        self.assertIn("crm_annual_savings", data)
        self.assertIn("total_annual_savings", data)
        self.assertIn("total_investment", data)
        self.assertIn("roi_percentage", data)
        self.assertIn("total_hours_saved_annually", data)
        self.assertIn("calculation_date", data)
        self.assertIn("calculation_id", data)
        
        # Verify calculations
        # Chatbot savings = (1000 * 0.6 * 4) / 60 * 5000 * 12 = 1,440,000 ARS annually
        expected_chatbot_monthly_hours_saved = (1000 * 0.6 * 4) / 60
        self.assertAlmostEqual(data["chatbot_monthly_hours_saved"], expected_chatbot_monthly_hours_saved, places=1)
        
        expected_chatbot_annual_savings = expected_chatbot_monthly_hours_saved * 5000 * 12
        self.assertAlmostEqual(data["chatbot_annual_savings"], expected_chatbot_annual_savings, places=1)
        
        # CRM savings = 40 * 0.5 * 3 * 12 * 5000 = 3,600,000 ARS annually
        expected_crm_annual_hours_saved = 40 * 0.5 * 3 * 12
        self.assertAlmostEqual(data["crm_annual_hours_saved"], expected_crm_annual_hours_saved, places=1)
        
        expected_crm_annual_savings = expected_crm_annual_hours_saved * 5000
        self.assertAlmostEqual(data["crm_annual_savings"], expected_crm_annual_savings, places=1)
        
        # Total savings = 1,440,000 + 3,600,000 = 5,040,000 ARS
        expected_total_annual_savings = expected_chatbot_annual_savings + expected_crm_annual_savings
        self.assertAlmostEqual(data["total_annual_savings"], expected_total_annual_savings, places=1)
        
        # Total investment = 200,000 + 1,000,000 = 1,200,000 ARS
        expected_total_investment = 200000 + 1000000
        self.assertEqual(data["total_investment"], expected_total_investment)
        
        # ROI = ((5,040,000 - 1,200,000) / 1,200,000) * 100 = 320%
        expected_roi_percentage = ((expected_total_annual_savings - expected_total_investment) / expected_total_investment) * 100
        self.assertAlmostEqual(data["roi_percentage"], expected_roi_percentage, places=1)
        
        # Verify additional_annual_revenue is None for basic calculation
        self.assertIsNone(data["additional_annual_revenue"])
        
        print("✅ Basic ROI calculation test passed")
    
    def test_roi_calculation_with_revenue_parameters(self):
        """Test with optional revenue fields"""
        payload = {
            "monthly_inquiries": 1000,
            "automation_percentage": 60,
            "minutes_per_inquiry": 4,
            "monthly_crm_hours": 40,
            "crm_automation_percentage": 50,
            "team_members": 3,
            "hourly_cost_ars": 5000,
            "bitrix24_annual_cost": 200000,
            "implementation_cost": 1000000,
            "average_ticket_ars": 15000,
            "current_conversion_rate": 2,
            "expected_conversion_rate": 3
        }
        
        response = requests.post(f"{API_BASE_URL}/calculate-roi", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify all required fields are present including additional_annual_revenue
        self.assertIn("additional_annual_revenue", data)
        self.assertIsNotNone(data["additional_annual_revenue"])
        
        # Calculate expected additional revenue
        conversion_improvement = (3 - 2) / 100  # (expected - current) / 100
        expected_additional_revenue = 1000 * conversion_improvement * 15000 * 12
        self.assertAlmostEqual(data["additional_annual_revenue"], expected_additional_revenue, places=1)
        
        print("✅ ROI calculation with revenue parameters test passed")
    
    def test_edge_cases(self):
        """Test with various edge cases"""
        
        # Test with low automation percentage (10%)
        low_automation_payload = {
            "monthly_inquiries": 1000,
            "automation_percentage": 10,
            "minutes_per_inquiry": 4,
            "monthly_crm_hours": 40,
            "crm_automation_percentage": 10,
            "team_members": 3,
            "hourly_cost_ars": 5000,
            "bitrix24_annual_cost": 200000,
            "implementation_cost": 1000000
        }
        
        response = requests.post(f"{API_BASE_URL}/calculate-roi", json=low_automation_payload)
        self.assertEqual(response.status_code, 200)
        low_auto_data = response.json()
        
        # Test with high automation percentage (90%)
        high_automation_payload = {
            "monthly_inquiries": 1000,
            "automation_percentage": 90,
            "minutes_per_inquiry": 4,
            "monthly_crm_hours": 40,
            "crm_automation_percentage": 90,
            "team_members": 3,
            "hourly_cost_ars": 5000,
            "bitrix24_annual_cost": 200000,
            "implementation_cost": 1000000
        }
        
        response = requests.post(f"{API_BASE_URL}/calculate-roi", json=high_automation_payload)
        self.assertEqual(response.status_code, 200)
        high_auto_data = response.json()
        
        # Verify high automation gives higher savings than low automation
        self.assertGreater(high_auto_data["total_annual_savings"], low_auto_data["total_annual_savings"])
        
        # Test with different team sizes
        team_sizes = [1, 5, 10]
        previous_savings = 0
        
        for team_size in team_sizes:
            team_payload = {
                "monthly_inquiries": 1000,
                "automation_percentage": 60,
                "minutes_per_inquiry": 4,
                "monthly_crm_hours": 40,
                "crm_automation_percentage": 50,
                "team_members": team_size,
                "hourly_cost_ars": 5000,
                "bitrix24_annual_cost": 200000,
                "implementation_cost": 1000000
            }
            
            response = requests.post(f"{API_BASE_URL}/calculate-roi", json=team_payload)
            self.assertEqual(response.status_code, 200)
            team_data = response.json()
            
            # Verify larger team size gives higher CRM savings
            if previous_savings > 0:
                self.assertGreater(team_data["crm_annual_savings"], previous_savings)
            
            previous_savings = team_data["crm_annual_savings"]
        
        # Test with different cost structures
        high_cost_payload = {
            "monthly_inquiries": 1000,
            "automation_percentage": 60,
            "minutes_per_inquiry": 4,
            "monthly_crm_hours": 40,
            "crm_automation_percentage": 50,
            "team_members": 3,
            "hourly_cost_ars": 10000,  # Higher hourly cost
            "bitrix24_annual_cost": 400000,  # Higher Bitrix cost
            "implementation_cost": 2000000  # Higher implementation cost
        }
        
        response = requests.post(f"{API_BASE_URL}/calculate-roi", json=high_cost_payload)
        self.assertEqual(response.status_code, 200)
        high_cost_data = response.json()
        
        # Verify higher costs affect the calculations correctly
        self.assertGreater(high_cost_data["total_investment"], 1200000)
        
        print("✅ Edge cases test passed")
    
    def test_mathematical_accuracy(self):
        """Verify the mathematical accuracy of calculations"""
        payload = {
            "monthly_inquiries": 1000,
            "automation_percentage": 60,
            "minutes_per_inquiry": 4,
            "monthly_crm_hours": 40,
            "crm_automation_percentage": 50,
            "team_members": 3,
            "hourly_cost_ars": 5000,
            "bitrix24_annual_cost": 200000,
            "implementation_cost": 1000000
        }
        
        response = requests.post(f"{API_BASE_URL}/calculate-roi", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Chatbot savings = (1000 * 0.6 * 4) / 60 * 5000 * 12 = 1,440,000 ARS annually
        expected_chatbot_monthly_hours = (1000 * 0.6 * 4) / 60
        expected_chatbot_annual_savings = expected_chatbot_monthly_hours * 5000 * 12
        
        # CRM savings = 40 * 0.5 * 3 * 12 * 5000 = 3,600,000 ARS annually
        expected_crm_annual_hours = 40 * 0.5 * 3 * 12
        expected_crm_annual_savings = expected_crm_annual_hours * 5000
        
        # Total savings = 1,440,000 + 3,600,000 = 5,040,000 ARS
        expected_total_savings = expected_chatbot_annual_savings + expected_crm_annual_savings
        
        # Total investment = 200,000 + 1,000,000 = 1,200,000 ARS
        expected_total_investment = 200000 + 1000000
        
        # ROI = ((5,040,000 - 1,200,000) / 1,200,000) * 100 = 320%
        expected_roi = ((expected_total_savings - expected_total_investment) / expected_total_investment) * 100
        
        # Total hours saved annually
        expected_total_hours = (expected_chatbot_monthly_hours * 12) + expected_crm_annual_hours
        
        # Verify all calculations match expected values
        self.assertAlmostEqual(data["chatbot_monthly_hours_saved"], expected_chatbot_monthly_hours, places=1)
        self.assertAlmostEqual(data["chatbot_annual_savings"], expected_chatbot_annual_savings, places=1)
        self.assertAlmostEqual(data["crm_annual_hours_saved"], expected_crm_annual_hours, places=1)
        self.assertAlmostEqual(data["crm_annual_savings"], expected_crm_annual_savings, places=1)
        self.assertAlmostEqual(data["total_annual_savings"], expected_total_savings, places=1)
        self.assertEqual(data["total_investment"], expected_total_investment)
        self.assertAlmostEqual(data["roi_percentage"], expected_roi, places=1)
        self.assertAlmostEqual(data["total_hours_saved_annually"], expected_total_hours, places=1)
        
        print("✅ Mathematical accuracy validation test passed")
    
    def test_error_handling(self):
        """Test with invalid data (negative numbers, missing required fields)"""
        
        # Test with negative values
        negative_payload = {
            "monthly_inquiries": -1000,
            "automation_percentage": 60,
            "minutes_per_inquiry": 4,
            "monthly_crm_hours": 40,
            "crm_automation_percentage": 50,
            "team_members": 3,
            "hourly_cost_ars": 5000,
            "bitrix24_annual_cost": 200000,
            "implementation_cost": 1000000
        }
        
        response = requests.post(f"{API_BASE_URL}/calculate-roi", json=negative_payload)
        # The API should either return an error or handle negative values gracefully
        if response.status_code == 400:
            # If API rejects negative values, that's acceptable
            print("✅ API correctly rejects negative values")
        else:
            # If API accepts negative values, ensure calculations are still mathematically correct
            self.assertEqual(response.status_code, 200)
            data = response.json()
            # Chatbot savings would be negative with negative inquiries
            self.assertLess(data["chatbot_annual_savings"], 0)
        
        # Test with missing required fields
        # The Pydantic model has default values, so we need to send an empty payload
        empty_payload = {}
        
        response = requests.post(f"{API_BASE_URL}/calculate-roi", json=empty_payload)
        # The API should use default values from the Pydantic model
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify default values are used
        self.assertEqual(data["inputs"]["monthly_inquiries"], 1000)
        self.assertEqual(data["inputs"]["automation_percentage"], 60.0)
        
        # Test with invalid types
        invalid_payload = {
            "monthly_inquiries": "not_a_number",
            "automation_percentage": 60,
            "minutes_per_inquiry": 4,
            "monthly_crm_hours": 40,
            "crm_automation_percentage": 50,
            "team_members": 3,
            "hourly_cost_ars": 5000,
            "bitrix24_annual_cost": 200000,
            "implementation_cost": 1000000
        }
        
        response = requests.post(f"{API_BASE_URL}/calculate-roi", json=invalid_payload)
        # The API should return a validation error
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity for validation errors
        
        print("✅ Error handling test passed")


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)