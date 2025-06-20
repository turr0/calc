from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime
import uuid

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ROICalculationRequest(BaseModel):
    monthly_inquiries: int = 1000
    automation_percentage: float = 60.0
    minutes_per_inquiry: int = 4
    monthly_crm_hours: int = 40
    crm_automation_percentage: float = 50.0
    team_members: int = 3
    hourly_cost_ars: int = 5000
    bitrix24_annual_cost: int = 200000
    implementation_cost: int = 1000000
    # Optional fields for revenue calculation
    average_ticket_ars: Optional[int] = None
    current_conversion_rate: Optional[float] = None
    expected_conversion_rate: Optional[float] = None

class ROICalculationResponse(BaseModel):
    # Input summary
    inputs: dict
    # Calculations
    chatbot_monthly_hours_saved: float
    chatbot_annual_savings: float
    crm_annual_hours_saved: float
    crm_annual_savings: float
    total_annual_savings: float
    total_investment: int
    roi_percentage: float
    # Optional revenue calculations
    additional_annual_revenue: Optional[float] = None
    # Summary
    total_hours_saved_annually: float
    calculation_date: str
    calculation_id: str

@app.post("/api/calculate-roi", response_model=ROICalculationResponse)
async def calculate_roi(request: ROICalculationRequest):
    try:
        # Chatbot savings calculations
        chatbot_monthly_hours_saved = (
            request.monthly_inquiries * 
            (request.automation_percentage / 100) * 
            request.minutes_per_inquiry
        ) / 60
        
        chatbot_annual_savings = (
            chatbot_monthly_hours_saved * 
            request.hourly_cost_ars * 
            12
        )
        
        # CRM automation savings calculations
        crm_annual_hours_saved = (
            request.monthly_crm_hours * 
            (request.crm_automation_percentage / 100) * 
            request.team_members * 
            12
        )
        
        crm_annual_savings = crm_annual_hours_saved * request.hourly_cost_ars
        
        # Total calculations
        total_annual_savings = chatbot_annual_savings + crm_annual_savings
        total_investment = request.bitrix24_annual_cost + request.implementation_cost
        
        # ROI calculation
        roi_percentage = ((total_annual_savings - total_investment) / total_investment) * 100
        
        # Optional revenue calculation
        additional_annual_revenue = None
        if (request.average_ticket_ars and 
            request.current_conversion_rate and 
            request.expected_conversion_rate):
            
            conversion_improvement = (
                request.expected_conversion_rate - request.current_conversion_rate
            ) / 100
            
            additional_annual_revenue = (
                request.monthly_inquiries * 
                conversion_improvement * 
                request.average_ticket_ars * 
                12
            )
        
        # Total hours saved
        total_hours_saved_annually = (chatbot_monthly_hours_saved * 12) + crm_annual_hours_saved
        
        return ROICalculationResponse(
            inputs={
                "monthly_inquiries": request.monthly_inquiries,
                "automation_percentage": request.automation_percentage,
                "minutes_per_inquiry": request.minutes_per_inquiry,
                "monthly_crm_hours": request.monthly_crm_hours,
                "crm_automation_percentage": request.crm_automation_percentage,
                "team_members": request.team_members,
                "hourly_cost_ars": request.hourly_cost_ars,
                "bitrix24_annual_cost": request.bitrix24_annual_cost,
                "implementation_cost": request.implementation_cost,
                "average_ticket_ars": request.average_ticket_ars,
                "current_conversion_rate": request.current_conversion_rate,
                "expected_conversion_rate": request.expected_conversion_rate,
            },
            chatbot_monthly_hours_saved=round(chatbot_monthly_hours_saved, 2),
            chatbot_annual_savings=round(chatbot_annual_savings, 2),
            crm_annual_hours_saved=round(crm_annual_hours_saved, 2),
            crm_annual_savings=round(crm_annual_savings, 2),
            total_annual_savings=round(total_annual_savings, 2),
            total_investment=total_investment,
            roi_percentage=round(roi_percentage, 2),
            additional_annual_revenue=round(additional_annual_revenue, 2) if additional_annual_revenue else None,
            total_hours_saved_annually=round(total_hours_saved_annually, 2),
            calculation_date=datetime.now().isoformat(),
            calculation_id=str(uuid.uuid4())
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "ROI Calculator API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)