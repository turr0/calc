from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import os
from datetime import datetime
import uuid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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
    bitrix24_plan: str = "Standard Plan"
    monthly_price_usd: int = 99
    implementation_cost: int = 1000000
    # Optional fields for revenue calculation
    average_ticket_ars: Optional[int] = None
    current_conversion_rate: Optional[float] = None
    expected_conversion_rate: Optional[float] = None
    # Email capture
    user_email: EmailStr
    company_name: Optional[str] = None

class ROICalculationResponse(BaseModel):
    # Input summary
    inputs: dict
    # Plan details
    selected_plan: str
    monthly_price_usd: int
    annual_license_cost_usd: int
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
    user_email: str

def send_roi_analysis_email(user_email: str, roi_data: dict, admin_email: str = "hola@efficiency.io"):
    """Send ROI analysis to both user and admin"""
    try:
        sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        if not sendgrid_api_key or sendgrid_api_key == "your_sendgrid_api_key_here":
            print("Warning: SendGrid API key not configured. Email functionality disabled.")
            return
        
        sg = SendGridAPIClient(sendgrid_api_key)
        sender_email = os.getenv('SENDER_EMAIL', 'hola@efficiency.io')
        
        # User email content
        user_subject = "Su Análisis ROI - Bitrix24 + Chatbot"
        user_html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333;">
                <div style="background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); color: white; padding: 30px; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px;">Efficiency24</h1>
                    <p style="margin: 10px 0 0 0; font-size: 16px;">Análisis ROI - Bitrix24 + Chatbot</p>
                </div>
                
                <div style="padding: 30px; background: #f8f9fa;">
                    <h2 style="color: #007bff; margin-bottom: 20px;">Resumen de su Análisis ROI</h2>
                    
                    <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <h3 style="color: #28a745; text-align: center; margin-bottom: 15px;">ROI Proyectado: {roi_data['roi_percentage']}%</h3>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                            <div style="text-align: center; padding: 15px; background: #e8f5e8; border-radius: 6px;">
                                <strong style="color: #28a745;">Ahorro Anual</strong><br>
                                <span style="font-size: 20px; color: #333;">${roi_data['total_annual_savings']:,.0f} ARS</span>
                            </div>
                            <div style="text-align: center; padding: 15px; background: #ffe8e8; border-radius: 6px;">
                                <strong style="color: #dc3545;">Inversión Total</strong><br>
                                <span style="font-size: 20px; color: #333;">${roi_data['total_investment']:,.0f} ARS</span>
                            </div>
                        </div>
                    </div>
                    
                    <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <h3 style="color: #007bff; margin-bottom: 15px;">Plan Bitrix24 Seleccionado</h3>
                        <p><strong>Plan:</strong> {roi_data['selected_plan']}</p>
                        <p><strong>Costo Mensual:</strong> ${roi_data['monthly_price_usd']} USD</p>
                        <p><strong>Costo Anual:</strong> ${roi_data['annual_license_cost_usd']} USD</p>
                    </div>
                    
                    <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <h3 style="color: #007bff; margin-bottom: 15px;">Desglose de Ahorros</h3>
                        <div style="margin-bottom: 15px; padding: 15px; background: #e3f2fd; border-radius: 6px;">
                            <strong>Ahorro por Chatbot:</strong> ${roi_data['chatbot_annual_savings']:,.0f} ARS/año<br>
                            <small style="color: #666;">({roi_data['chatbot_monthly_hours_saved'] * 12:.1f} horas ahorradas anualmente)</small>
                        </div>
                        <div style="margin-bottom: 15px; padding: 15px; background: #e8f5e8; border-radius: 6px;">
                            <strong>Ahorro por CRM:</strong> ${roi_data['crm_annual_savings']:,.0f} ARS/año<br>
                            <small style="color: #666;">({roi_data['crm_annual_hours_saved']:.1f} horas ahorradas anualmente)</small>
                        </div>
                        <div style="padding: 15px; background: #fff3cd; border-radius: 6px;">
                            <strong>Total Horas Ahorradas:</strong> {roi_data['total_hours_saved_annually']:.1f} horas/año
                        </div>
                    </div>
                    
                    {"<div style='background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;'><h3 style='color: #007bff; margin-bottom: 15px;'>Ingresos Adicionales Estimados</h3><p style='font-size: 18px; color: #28a745;'><strong>${roi_data['additional_annual_revenue']:,.0f} ARS/año</strong></p><p style='color: #666;'>Por mejora en tasa de conversión</p></div>" if roi_data.get('additional_annual_revenue') else ""}
                    
                    <div style="background: #007bff; color: white; padding: 20px; border-radius: 8px; text-align: center;">
                        <h3 style="margin: 0 0 10px 0;">¿Listo para dar el siguiente paso?</h3>
                        <p style="margin: 0; font-size: 14px;">Nuestro equipo se pondrá en contacto contigo para analizar estos resultados y ayudarte a implementar la solución perfecta para tu PyME.</p>
                    </div>
                </div>
                
                <div style="background: #333; color: #ccc; padding: 20px; text-align: center; font-size: 12px;">
                    <p style="margin: 0;">© 2024 Efficiency24. Todos los derechos reservados.</p>
                    <p style="margin: 5px 0 0 0;">Análisis generado el {roi_data['calculation_date'][:10]}</p>
                </div>
            </body>
        </html>
        """
        
        # Admin notification email
        admin_subject = f"Nueva Consulta ROI - {roi_data.get('company_name', 'Sin especificar')}"
        admin_html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: #007bff; color: white; padding: 20px;">
                    <h1 style="margin: 0;">Nueva Consulta ROI Recibida</h1>
                </div>
                
                <div style="padding: 20px; background: #f8f9fa;">
                    <h2>Información del Lead</h2>
                    <p><strong>Email:</strong> {user_email}</p>
                    <p><strong>Empresa:</strong> {roi_data.get('company_name', 'No especificada')}</p>
                    <p><strong>Fecha:</strong> {roi_data['calculation_date']}</p>
                    <p><strong>ID de Cálculo:</strong> {roi_data['calculation_id']}</p>
                    
                    <h3>Resultados ROI</h3>
                    <ul>
                        <li><strong>ROI:</strong> {roi_data['roi_percentage']}%</li>
                        <li><strong>Ahorro Anual:</strong> ${roi_data['total_annual_savings']:,.0f} ARS</li>
                        <li><strong>Inversión Total:</strong> ${roi_data['total_investment']:,.0f} ARS</li>
                        <li><strong>Plan Bitrix24:</strong> {roi_data['selected_plan']} (${roi_data['monthly_price_usd']}/mes)</li>
                        <li><strong>Horas Ahorradas/Año:</strong> {roi_data['total_hours_saved_annually']:.1f}</li>
                    </ul>
                    
                    <h3>Parámetros de Entrada</h3>
                    <ul>
                        <li><strong>Consultas mensuales:</strong> {roi_data['inputs']['monthly_inquiries']}</li>
                        <li><strong>% Automatización chatbot:</strong> {roi_data['inputs']['automation_percentage']}%</li>
                        <li><strong>Minutos por consulta:</strong> {roi_data['inputs']['minutes_per_inquiry']}</li>
                        <li><strong>Horas CRM mensuales:</strong> {roi_data['inputs']['monthly_crm_hours']}</li>
                        <li><strong>% Automatización CRM:</strong> {roi_data['inputs']['crm_automation_percentage']}%</li>
                        <li><strong>Miembros del equipo:</strong> {roi_data['inputs']['team_members']}</li>
                        <li><strong>Costo por hora:</strong> ${roi_data['inputs']['hourly_cost_ars']} ARS</li>
                    </ul>
                    
                    {"<h3>Proyección de Ingresos</h3><ul><li><strong>Ticket promedio:</strong> $" + str(roi_data['inputs'].get('average_ticket_ars', 'N/A')) + " ARS</li><li><strong>Conversión actual:</strong> " + str(roi_data['inputs'].get('current_conversion_rate', 'N/A')) + "%</li><li><strong>Conversión esperada:</strong> " + str(roi_data['inputs'].get('expected_conversion_rate', 'N/A')) + "%</li><li><strong>Ingresos adicionales:</strong> $" + str(roi_data.get('additional_annual_revenue', 0)) + " ARS/año</li></ul>" if roi_data.get('additional_annual_revenue') else ""}
                </div>
            </body>
        </html>
        """
        
        # Send email to user
        user_message = Mail(
            from_email=sender_email,
            to_emails=user_email,
            subject=user_subject,
            html_content=user_html_content
        )
        
        # Send email to admin
        admin_message = Mail(
            from_email=sender_email,
            to_emails=admin_email,
            subject=admin_subject,
            html_content=admin_html_content
        )
        
        # Send both emails
        sg.send(user_message)
        sg.send(admin_message)
        
        print(f"ROI analysis emails sent successfully to {user_email} and {admin_email}")
        
    except Exception as e:
        print(f"Error sending ROI analysis email: {str(e)}")

@app.post("/api/calculate-roi", response_model=ROICalculationResponse)
async def calculate_roi(request: ROICalculationRequest, background_tasks: BackgroundTasks):
    try:
        # Calculate annual license cost from monthly price
        annual_license_cost_usd = request.monthly_price_usd * 12
        
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
        # Convert USD license cost to ARS (approximate rate: 1 USD = 800 ARS as of 2024)
        annual_license_cost_ars = annual_license_cost_usd * 800
        total_investment = annual_license_cost_ars + request.implementation_cost
        
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
        
        # Prepare response
        response_data = ROICalculationResponse(
            inputs={
                "monthly_inquiries": request.monthly_inquiries,
                "automation_percentage": request.automation_percentage,
                "minutes_per_inquiry": request.minutes_per_inquiry,
                "monthly_crm_hours": request.monthly_crm_hours,
                "crm_automation_percentage": request.crm_automation_percentage,
                "team_members": request.team_members,
                "hourly_cost_ars": request.hourly_cost_ars,
                "bitrix24_plan": request.bitrix24_plan,
                "monthly_price_usd": request.monthly_price_usd,
                "implementation_cost": request.implementation_cost,
                "average_ticket_ars": request.average_ticket_ars,
                "current_conversion_rate": request.current_conversion_rate,
                "expected_conversion_rate": request.expected_conversion_rate,
                "company_name": request.company_name,
            },
            selected_plan=request.bitrix24_plan,
            monthly_price_usd=request.monthly_price_usd,
            annual_license_cost_usd=annual_license_cost_usd,
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
            calculation_id=str(uuid.uuid4()),
            user_email=request.user_email
        )
        
        # Send emails in background
        background_tasks.add_task(
            send_roi_analysis_email,
            request.user_email,
            response_data.dict(),
            "hola@efficiency.io"
        )
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "ROI Calculator API is running"}

@app.get("/api/bitrix24-plans")
async def get_bitrix24_plans():
    """Get available Bitrix24 plans with pricing"""
    return {
        "plans": [
            {"name": "Basic Plan", "monthly_price_usd": 49, "description": "Essential CRM features for small teams"},
            {"name": "Standard Plan", "monthly_price_usd": 99, "description": "Advanced automation and reporting", "default": True},
            {"name": "Professional Plan", "monthly_price_usd": 199, "description": "Complete business solution with integrations"},
            {"name": "Enterprise Plan", "monthly_price_usd": 399, "description": "Full-scale enterprise solution with premium support"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)