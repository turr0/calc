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
    
    def test_bitrix24_plans_endpoint(self):
        """Test the /api/bitrix24-plans endpoint to ensure it returns the correct plan data"""
        response = requests.get(f"{API_BASE_URL}/bitrix24-plans")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify the response structure
        self.assertIn("plans", data)
        plans = data["plans"]
        self.assertEqual(len(plans), 4)  # Should have 4 plans
        
        # Verify each plan has the correct structure and data
        expected_plans = [
            {"name": "Basic Plan", "monthly_price_usd": 49, "description": "Essential CRM features for small teams"},
            {"name": "Standard Plan", "monthly_price_usd": 99, "description": "Advanced automation and reporting", "default": True},
            {"name": "Professional Plan", "monthly_price_usd": 199, "description": "Complete business solution with integrations"},
            {"name": "Enterprise Plan", "monthly_price_usd": 399, "description": "Full-scale enterprise solution with premium support"}
        ]
        
        for i, plan in enumerate(plans):
            self.assertEqual(plan["name"], expected_plans[i]["name"])
            self.assertEqual(plan["monthly_price_usd"], expected_plans[i]["monthly_price_usd"])
            self.assertEqual(plan["description"], expected_plans[i]["description"])
            
            # Check if this is the default plan (Standard Plan)
            if plan["name"] == "Standard Plan":
                self.assertTrue(plan["default"])
        
        print("✅ Bitrix24 plans endpoint test passed")
    
    def test_roi_calculation_with_standard_plan(self):
        """Test /api/calculate-roi with Standard Plan (default)"""
        payload = {
            "monthly_inquiries": 1000,
            "automation_percentage": 60,
            "minutes_per_inquiry": 4,
            "monthly_crm_hours": 40,
            "crm_automation_percentage": 50,
            "team_members": 3,
            "hourly_cost_ars": 5000,
            "bitrix24_plan": "Standard Plan",
            "monthly_price_usd": 99,
            "implementation_cost": 1000000
        }
        
        response = requests.post(f"{API_BASE_URL}/calculate-roi", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify all required fields are present
        self.assertIn("inputs", data)
        self.assertIn("selected_plan", data)
        self.assertIn("monthly_price_usd", data)
        self.assertIn("annual_license_cost_usd", data)
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
        
        # Verify plan details
        self.assertEqual(data["selected_plan"], "Standard Plan")
        self.assertEqual(data["monthly_price_usd"], 99)
        self.assertEqual(data["annual_license_cost_usd"], 99 * 12)  # 1188 USD
        
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
        
        # Total investment = (99 * 12 * 800) + 1,000,000 = 950,400 + 1,000,000 = 1,950,400 ARS
        expected_annual_license_cost_ars = 99 * 12 * 800  # 1188 USD * 800 = 950,400 ARS
        expected_total_investment = expected_annual_license_cost_ars + 1000000
        self.assertEqual(data["total_investment"], expected_total_investment)
        
        # ROI = ((5,040,000 - 1,950,400) / 1,950,400) * 100
        expected_roi_percentage = ((expected_total_annual_savings - expected_total_investment) / expected_total_investment) * 100
        self.assertAlmostEqual(data["roi_percentage"], expected_roi_percentage, places=1)
        
        # Verify additional_annual_revenue is None for basic calculation
        self.assertIsNone(data["additional_annual_revenue"])
        
        print("✅ ROI calculation with Standard Plan test passed")
    
    def test_roi_calculation_with_different_plans(self):
        """Test ROI calculation with different Bitrix24 plans"""
        plans = [
            {"name": "Basic Plan", "monthly_price_usd": 49},
            {"name": "Professional Plan", "monthly_price_usd": 199},
            {"name": "Enterprise Plan", "monthly_price_usd": 399}
        ]
        
        for plan in plans:
            payload = {
                "monthly_inquiries": 1000,
                "automation_percentage": 60,
                "minutes_per_inquiry": 4,
                "monthly_crm_hours": 40,
                "crm_automation_percentage": 50,
                "team_members": 3,
                "hourly_cost_ars": 5000,
                "bitrix24_plan": plan["name"],
                "monthly_price_usd": plan["monthly_price_usd"],
                "implementation_cost": 1000000
            }
            
            response = requests.post(f"{API_BASE_URL}/calculate-roi", json=payload)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            
            # Verify plan details
            self.assertEqual(data["selected_plan"], plan["name"])
            self.assertEqual(data["monthly_price_usd"], plan["monthly_price_usd"])
            self.assertEqual(data["annual_license_cost_usd"], plan["monthly_price_usd"] * 12)
            
            # Verify total investment calculation
            expected_annual_license_cost_ars = plan["monthly_price_usd"] * 12 * 800
            expected_total_investment = expected_annual_license_cost_ars + 1000000
            self.assertEqual(data["total_investment"], expected_total_investment)
            
            # Verify ROI calculation
            expected_chatbot_monthly_hours_saved = (1000 * 0.6 * 4) / 60
            expected_chatbot_annual_savings = expected_chatbot_monthly_hours_saved * 5000 * 12
            expected_crm_annual_hours_saved = 40 * 0.5 * 3 * 12
            expected_crm_annual_savings = expected_crm_annual_hours_saved * 5000
            expected_total_annual_savings = expected_chatbot_annual_savings + expected_crm_annual_savings
            expected_roi_percentage = ((expected_total_annual_savings - expected_total_investment) / expected_total_investment) * 100
            self.assertAlmostEqual(data["roi_percentage"], expected_roi_percentage, places=1)
        
        print("✅ ROI calculation with different plans test passed")
    
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
            "bitrix24_plan": "Standard Plan",
            "monthly_price_usd": 99,
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
        
        # Verify plan details and total investment calculation
        self.assertEqual(data["selected_plan"], "Standard Plan")
        self.assertEqual(data["monthly_price_usd"], 99)
        self.assertEqual(data["annual_license_cost_usd"], 99 * 12)
        
        expected_annual_license_cost_ars = 99 * 12 * 800
        expected_total_investment = expected_annual_license_cost_ars + 1000000
        self.assertEqual(data["total_investment"], expected_total_investment)
        
        print("✅ ROI calculation with revenue parameters test passed")
    
    def test_mathematical_accuracy(self):
        """Verify the mathematical accuracy of calculations with the new plan structure"""
        payload = {
            "monthly_inquiries": 1000,
            "automation_percentage": 60,
            "minutes_per_inquiry": 4,
            "monthly_crm_hours": 40,
            "crm_automation_percentage": 50,
            "team_members": 3,
            "hourly_cost_ars": 5000,
            "bitrix24_plan": "Standard Plan",
            "monthly_price_usd": 99,
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
        
        # Annual license cost = 99 * 12 = 1,188 USD
        expected_annual_license_cost_usd = 99 * 12
        
        # Total investment = (1,188 * 800) + 1,000,000 = 950,400 + 1,000,000 = 1,950,400 ARS
        expected_annual_license_cost_ars = expected_annual_license_cost_usd * 800
        expected_total_investment = expected_annual_license_cost_ars + 1000000
        
        # ROI = ((5,040,000 - 1,950,400) / 1,950,400) * 100
        expected_roi = ((expected_total_savings - expected_total_investment) / expected_total_investment) * 100
        
        # Total hours saved annually
        expected_total_hours = (expected_chatbot_monthly_hours * 12) + expected_crm_annual_hours
        
        # Verify all calculations match expected values
        self.assertEqual(data["annual_license_cost_usd"], expected_annual_license_cost_usd)
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
            "bitrix24_plan": "Standard Plan",
            "monthly_price_usd": 99,
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
        self.assertEqual(data["inputs"]["bitrix24_plan"], "Standard Plan")
        self.assertEqual(data["inputs"]["monthly_price_usd"], 99)
        
        # Test with invalid types
        invalid_payload = {
            "monthly_inquiries": "not_a_number",
            "automation_percentage": 60,
            "minutes_per_inquiry": 4,
            "monthly_crm_hours": 40,
            "crm_automation_percentage": 50,
            "team_members": 3,
            "hourly_cost_ars": 5000,
            "bitrix24_plan": "Standard Plan",
            "monthly_price_usd": 99,
            "implementation_cost": 1000000
        }
        
        response = requests.post(f"{API_BASE_URL}/calculate-roi", json=invalid_payload)
        # The API should return a validation error
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity for validation errors
        
        print("✅ Error handling test passed")


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)