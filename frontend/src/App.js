import React, { useState } from 'react';
import './App.css';

const App = () => {
  // Bitrix24 plans data
  const bitrix24Plans = [
    { name: "Basic Plan", monthly_price_usd: 49, description: "Essential CRM features for small teams" },
    { name: "Standard Plan", monthly_price_usd: 99, description: "Advanced automation and reporting" },
    { name: "Professional Plan", monthly_price_usd: 199, description: "Complete business solution with integrations" },
    { name: "Enterprise Plan", monthly_price_usd: 399, description: "Full-scale enterprise solution with premium support" }
  ];

  const [formData, setFormData] = useState({
    monthly_inquiries: 1000,
    automation_percentage: 60,
    minutes_per_inquiry: 4,
    monthly_crm_hours: 40,
    crm_automation_percentage: 50,
    team_members: 3,
    hourly_cost_ars: 5000,
    bitrix24_plan: "Standard Plan",
    monthly_price_usd: 99,
    implementation_cost: 1000000,
    average_ticket_ars: '',
    current_conversion_rate: '',
    expected_conversion_rate: ''
  });

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value === '' ? '' : Number(value)
    }));
  };

  const handlePlanChange = (e) => {
    const selectedPlanName = e.target.value;
    const selectedPlan = bitrix24Plans.find(plan => plan.name === selectedPlanName);
    
    setFormData(prev => ({
      ...prev,
      bitrix24_plan: selectedPlanName,
      monthly_price_usd: selectedPlan.monthly_price_usd
    }));
  };

  const formatCurrency = (amount) => {
    if (!amount) return 'ARS $0';
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const formatUSD = (amount) => {
    if (!amount) return 'USD $0';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const formatHours = (hours) => {
    return new Intl.NumberFormat('es-AR', {
      minimumFractionDigits: 1,
      maximumFractionDigits: 1
    }).format(hours);
  };

  const calculateROI = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      
      // Prepare data, converting empty strings to null for optional fields
      const requestData = {
        ...formData,
        average_ticket_ars: formData.average_ticket_ars === '' ? null : formData.average_ticket_ars,
        current_conversion_rate: formData.current_conversion_rate === '' ? null : formData.current_conversion_rate,
        expected_conversion_rate: formData.expected_conversion_rate === '' ? null : formData.expected_conversion_rate
      };

      const response = await fetch(`${backendUrl}/api/calculate-roi`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(`Error al calcular ROI: ${err.message}`);
      console.error('Calculation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getSelectedPlan = () => {
    return bitrix24Plans.find(plan => plan.name === formData.bitrix24_plan);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">E24</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Efficiency24</h1>
                <p className="text-sm text-gray-600">Calculadora ROI Bitrix24 + Chatbot</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Information Section */}
        <div className="mb-12">
          <div className="bg-white rounded-xl shadow-lg p-6 md:p-8 border-l-4 border-blue-500">
            <div className="max-w-6xl mx-auto">
              <h3 className="text-xl md:text-2xl font-bold text-gray-900 mb-6 md:mb-8 text-center">
                Ahorros de Tiempo Basados en Estudios de la Industria
              </h3>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8">
                {/* Chatbot Section */}
                <div className="bg-blue-50 rounded-lg p-4 md:p-6 border border-blue-100">
                  <div className="flex items-center mb-4">
                    <div className="w-10 h-10 md:w-12 md:h-12 bg-blue-600 rounded-lg flex items-center justify-center mr-3 md:mr-4 flex-shrink-0">
                      <svg className="w-5 h-5 md:w-6 md:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                      </svg>
                    </div>
                    <h4 className="text-lg md:text-xl font-semibold text-blue-900">
                      Reducción de Tiempo con Chatbot
                    </h4>
                  </div>
                  
                  <div className="space-y-3 text-blue-800">
                    <p className="flex items-start">
                      <span className="inline-block w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Los chatbots automatizan típicamente <strong>60% a 80%</strong> de las consultas de clientes</span>
                    </p>
                    <p className="flex items-start">
                      <span className="inline-block w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Ahorro promedio de <strong>3 a 5 minutos por consulta</strong></span>
                    </p>
                    <p className="flex items-start">
                      <span className="inline-block w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Resultado: <strong>cientos de horas ahorradas por año</strong> para PyMEs</span>
                    </p>
                  </div>
                  
                  <div className="mt-4 p-3 bg-blue-100 rounded-md">
                    <p className="text-sm text-blue-700">
                      <strong>Fuente:</strong> Estudios de IBM e Intercom sobre automatización de atención al cliente
                    </p>
                  </div>
                </div>

                {/* CRM Section */}
                <div className="bg-green-50 rounded-lg p-4 md:p-6 border border-green-100">
                  <div className="flex items-center mb-4">
                    <div className="w-10 h-10 md:w-12 md:h-12 bg-green-600 rounded-lg flex items-center justify-center mr-3 md:mr-4 flex-shrink-0">
                      <svg className="w-5 h-5 md:w-6 md:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                    </div>
                    <h4 className="text-lg md:text-xl font-semibold text-green-900">
                      Reducción de Tiempo con Bitrix24 CRM
                    </h4>
                  </div>
                  
                  <div className="space-y-3 text-green-800">
                    <p className="flex items-start">
                      <span className="inline-block w-2 h-2 bg-green-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Automatiza tareas administrativas, de ventas y soporte</span>
                    </p>
                    <p className="flex items-start">
                      <span className="inline-block w-2 h-2 bg-green-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Reduce la carga manual en <strong>30% a 50%</strong> en promedio</span>
                    </p>
                    <p className="flex items-start">
                      <span className="inline-block w-2 h-2 bg-green-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Mejora significativa en seguimiento y reportes automáticos</span>
                    </p>
                  </div>
                  
                  <div className="mt-4 p-3 bg-green-100 rounded-md">
                    <p className="text-sm text-green-700">
                      <strong>Fuente:</strong> Nucleus Research - Estudios sobre ROI de sistemas CRM
                    </p>
                  </div>
                </div>
              </div>

              {/* Additional Context */}
              <div className="mt-6 md:mt-8 bg-gray-50 rounded-lg p-4 md:p-6 border border-gray-200">
                <div className="text-center">
                  <h5 className="text-lg font-semibold text-gray-900 mb-3">
                    ¿Por Qué Estos Datos Son Importantes?
                  </h5>
                  <p className="text-gray-700 leading-relaxed max-w-4xl mx-auto text-sm md:text-base">
                    Esta calculadora utiliza datos reales de estudios industriales para proyectar ahorros realistas. 
                    Los valores por defecto están basados en promedios de PyMEs argentinas que han implementado 
                    soluciones similares, proporcionando estimaciones conservadoras y alcanzables para su organización.
                  </p>
                </div>
                
                <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                    <div className="text-xl md:text-2xl font-bold text-blue-600 mb-1">60-80%</div>
                    <div className="text-xs md:text-sm text-gray-600">Consultas automatizables</div>
                  </div>
                  <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                    <div className="text-xl md:text-2xl font-bold text-green-600 mb-1">30-50%</div>
                    <div className="text-xs md:text-sm text-gray-600">Reducción carga CRM</div>
                  </div>
                  <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                    <div className="text-xl md:text-2xl font-bold text-purple-600 mb-1">3-5 min</div>
                    <div className="text-xs md:text-sm text-gray-600">Ahorro por consulta</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">
              Parámetros de Cálculo
            </h2>
            
            <div className="space-y-6">
              {/* Customer Service Automation */}
              <div className="border-l-4 border-blue-500 pl-4">
                <h3 className="font-medium text-gray-900 mb-4">Automatización de Atención al Cliente</h3>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Consultas mensuales
                    </label>
                    <input
                      type="number"
                      name="monthly_inquiries"
                      value={formData.monthly_inquiries}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      % Automatizable por chatbot
                    </label>
                    <input
                      type="number"
                      name="automation_percentage"
                      value={formData.automation_percentage}
                      onChange={handleInputChange}
                      min="0"
                      max="100"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div className="sm:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Tiempo promedio por consulta (minutos)
                    </label>
                    <input
                      type="number"
                      name="minutes_per_inquiry"
                      value={formData.minutes_per_inquiry}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
              </div>

              {/* CRM Automation */}
              <div className="border-l-4 border-green-500 pl-4">
                <h3 className="font-medium text-gray-900 mb-4">Automatización CRM</h3>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Horas al mes en gestión y seguimiento manual de clientes y ventas
                    </label>
                    <input
                      type="number"
                      name="monthly_crm_hours"
                      value={formData.monthly_crm_hours}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      % Automatizable CRM
                    </label>
                    <input
                      type="number"
                      name="crm_automation_percentage"
                      value={formData.crm_automation_percentage}
                      onChange={handleInputChange}
                      min="0"
                      max="100"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div className="sm:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Miembros del equipo
                    </label>
                    <input
                      type="number"
                      name="team_members"
                      value={formData.team_members}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
              </div>

              {/* Cost Parameters */}
              <div className="border-l-4 border-purple-500 pl-4">
                <h3 className="font-medium text-gray-900 mb-4">Parámetros de Costo</h3>
                
                <div className="grid grid-cols-1 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Costo por hora empleado (ARS)
                    </label>
                    <input
                      type="number"
                      name="hourly_cost_ars"
                      value={formData.hourly_cost_ars}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Plan Bitrix24
                    </label>
                    <select
                      name="bitrix24_plan"
                      value={formData.bitrix24_plan}
                      onChange={handlePlanChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                    >
                      {bitrix24Plans.map((plan) => (
                        <option key={plan.name} value={plan.name}>
                          {plan.name} - {formatUSD(plan.monthly_price_usd)}/mes
                        </option>
                      ))}
                    </select>
                    <div className="mt-2 p-3 bg-blue-50 rounded-md">
                      <div className="text-sm">
                        <div className="font-medium text-blue-900">Plan seleccionado: {formData.bitrix24_plan}</div>
                        <div className="text-blue-700">Precio mensual: {formatUSD(formData.monthly_price_usd)}</div>
                        <div className="text-blue-700">Costo anual: {formatUSD(formData.monthly_price_usd * 12)}</div>
                        <div className="text-blue-600 text-xs mt-1">
                          {getSelectedPlan()?.description}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Revenue Parameters (Optional) */}
              <div className="border-l-4 border-orange-500 pl-4">
                <h3 className="font-medium text-gray-900 mb-4">Parámetros de Ingresos (Opcional)</h3>
                
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Ticket promedio (ARS)
                    </label>
                    <input
                      type="number"
                      name="average_ticket_ars"
                      value={formData.average_ticket_ars}
                      onChange={handleInputChange}
                      placeholder="Opcional"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Conversión actual (%)
                    </label>
                    <input
                      type="number"
                      name="current_conversion_rate"
                      value={formData.current_conversion_rate}
                      onChange={handleInputChange}
                      placeholder="Opcional"
                      step="0.1"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Conversión esperada (%)
                    </label>
                    <input
                      type="number"
                      name="expected_conversion_rate"
                      value={formData.expected_conversion_rate}
                      onChange={handleInputChange}
                      placeholder="Opcional"
                      step="0.1"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
              </div>
            </div>

            <button
              onClick={calculateROI}
              disabled={loading}
              className="w-full mt-8 bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Calculando...' : 'Calcular ROI'}
            </button>

            {error && (
              <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                {error}
              </div>
            )}
          </div>

          {/* Results */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">
              Resultados del Análisis ROI
            </h2>
            
            {!results ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                </div>
                <p className="text-gray-500">
                  Complete los parámetros y haga clic en "Calcular ROI" para ver los resultados.
                </p>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Plan Selection Summary */}
                <div className="bg-indigo-50 rounded-lg p-4">
                  <h4 className="font-medium text-indigo-900 mb-2">Plan Bitrix24 Seleccionado</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-sm">
                    <div>
                      <span className="text-indigo-700 font-medium">{results.selected_plan}</span>
                    </div>
                    <div>
                      <span className="text-indigo-600">Mensual: {formatUSD(results.monthly_price_usd)}</span>
                    </div>
                    <div>
                      <span className="text-indigo-600">Anual: {formatUSD(results.annual_license_cost_usd)}</span>
                    </div>
                  </div>
                </div>

                {/* ROI Summary */}
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-6 text-white">
                  <div className="text-center">
                    <h3 className="text-lg font-medium mb-2">ROI Proyectado</h3>
                    <div className="text-4xl font-bold mb-2">
                      {results.roi_percentage > 0 ? '+' : ''}{results.roi_percentage}%
                    </div>
                    <p className="text-blue-100">Retorno sobre la inversión anual</p>
                  </div>
                </div>

                {/* Key Metrics */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="bg-green-50 rounded-lg p-4">
                    <h4 className="font-medium text-green-900 mb-2">Ahorro Total Anual</h4>
                    <div className="text-2xl font-bold text-green-600">
                      {formatCurrency(results.total_annual_savings)}
                    </div>
                  </div>
                  
                  <div className="bg-red-50 rounded-lg p-4">
                    <h4 className="font-medium text-red-900 mb-2">Inversión Total</h4>
                    <div className="text-2xl font-bold text-red-600">
                      {formatCurrency(results.total_investment)}
                    </div>
                    <div className="text-sm text-red-700 mt-1">
                      Implementación + Licencia anual ({formatUSD(results.annual_license_cost_usd)})
                    </div>
                  </div>
                </div>

                {/* Detailed Breakdown */}
                <div className="space-y-4">
                  <h4 className="font-medium text-gray-900">Desglose de Ahorros</h4>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-gray-700">Ahorro por Chatbot</span>
                      <span className="font-medium">{formatCurrency(results.chatbot_annual_savings)}</span>
                    </div>
                    <div className="text-sm text-gray-600">
                      {formatHours(results.chatbot_monthly_hours_saved * 12)} horas anuales
                    </div>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-gray-700">Ahorro por CRM</span>
                      <span className="font-medium">{formatCurrency(results.crm_annual_savings)}</span>
                    </div>
                    <div className="text-sm text-gray-600">
                      {formatHours(results.crm_annual_hours_saved)} horas anuales
                    </div>
                  </div>
                </div>

                {/* Revenue Impact */}
                {results.additional_annual_revenue && (
                  <div className="bg-blue-50 rounded-lg p-4">
                    <h4 className="font-medium text-blue-900 mb-2">Ingresos Adicionales Estimados</h4>
                    <div className="text-2xl font-bold text-blue-600">
                      {formatCurrency(results.additional_annual_revenue)}
                    </div>
                    <p className="text-sm text-blue-700 mt-1">
                      Por mejora en tasa de conversión
                    </p>
                  </div>
                )}

                {/* Summary Stats */}
                <div className="border-t pt-4">
                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold text-gray-900">
                        {formatHours(results.total_hours_saved_annually)}
                      </div>
                      <div className="text-sm text-gray-600">Horas ahorradas/año</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-gray-900">
                        {Math.max(1, Math.round(results.total_investment / Math.max(1, results.total_annual_savings) * 12))}
                      </div>
                      <div className="text-sm text-gray-600">Meses para recuperar inversión</div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Information Section */}
        <div className="mt-12">
          <div className="bg-white rounded-xl shadow-lg p-6 md:p-8 border-l-4 border-blue-500">
            <div className="max-w-6xl mx-auto">
              <h3 className="text-xl md:text-2xl font-bold text-gray-900 mb-6 md:mb-8 text-center">
                Ahorros de Tiempo Basados en Estudios de la Industria
              </h3>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8">
                {/* Chatbot Section */}
                <div className="bg-blue-50 rounded-lg p-4 md:p-6 border border-blue-100">
                  <div className="flex items-center mb-4">
                    <div className="w-10 h-10 md:w-12 md:h-12 bg-blue-600 rounded-lg flex items-center justify-center mr-3 md:mr-4 flex-shrink-0">
                      <svg className="w-5 h-5 md:w-6 md:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                      </svg>
                    </div>
                    <h4 className="text-lg md:text-xl font-semibold text-blue-900">
                      Reducción de Tiempo con Chatbot
                    </h4>
                  </div>
                  
                  <div className="space-y-3 text-blue-800">
                    <p className="flex items-start">
                      <span className="inline-block w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Los chatbots automatizan típicamente <strong>60% a 80%</strong> de las consultas de clientes</span>
                    </p>
                    <p className="flex items-start">
                      <span className="inline-block w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Ahorro promedio de <strong>3 a 5 minutos por consulta</strong></span>
                    </p>
                    <p className="flex items-start">
                      <span className="inline-block w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Resultado: <strong>cientos de horas ahorradas por año</strong> para PyMEs</span>
                    </p>
                  </div>
                  
                  <div className="mt-4 p-3 bg-blue-100 rounded-md">
                    <p className="text-sm text-blue-700">
                      <strong>Fuente:</strong> Estudios de IBM e Intercom sobre automatización de atención al cliente
                    </p>
                  </div>
                </div>

                {/* CRM Section */}
                <div className="bg-green-50 rounded-lg p-4 md:p-6 border border-green-100">
                  <div className="flex items-center mb-4">
                    <div className="w-10 h-10 md:w-12 md:h-12 bg-green-600 rounded-lg flex items-center justify-center mr-3 md:mr-4 flex-shrink-0">
                      <svg className="w-5 h-5 md:w-6 md:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                    </div>
                    <h4 className="text-lg md:text-xl font-semibold text-green-900">
                      Reducción de Tiempo con Bitrix24 CRM
                    </h4>
                  </div>
                  
                  <div className="space-y-3 text-green-800">
                    <p className="flex items-start">
                      <span className="inline-block w-2 h-2 bg-green-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Automatiza tareas administrativas, de ventas y soporte</span>
                    </p>
                    <p className="flex items-start">
                      <span className="inline-block w-2 h-2 bg-green-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Reduce la carga manual en <strong>30% a 50%</strong> en promedio</span>
                    </p>
                    <p className="flex items-start">
                      <span className="inline-block w-2 h-2 bg-green-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Mejora significativa en seguimiento y reportes automáticos</span>
                    </p>
                  </div>
                  
                  <div className="mt-4 p-3 bg-green-100 rounded-md">
                    <p className="text-sm text-green-700">
                      <strong>Fuente:</strong> Nucleus Research - Estudios sobre ROI de sistemas CRM
                    </p>
                  </div>
                </div>
              </div>

              {/* Additional Context */}
              <div className="mt-6 md:mt-8 bg-gray-50 rounded-lg p-4 md:p-6 border border-gray-200">
                <div className="text-center">
                  <h5 className="text-lg font-semibold text-gray-900 mb-3">
                    ¿Por Qué Estos Datos Son Importantes?
                  </h5>
                  <p className="text-gray-700 leading-relaxed max-w-4xl mx-auto text-sm md:text-base">
                    Esta calculadora utiliza datos reales de estudios industriales para proyectar ahorros realistas. 
                    Los valores por defecto están basados en promedios de PyMEs argentinas que han implementado 
                    soluciones similares, proporcionando estimaciones conservadoras y alcanzables para su organización.
                  </p>
                </div>
                
                <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                    <div className="text-xl md:text-2xl font-bold text-blue-600 mb-1">60-80%</div>
                    <div className="text-xs md:text-sm text-gray-600">Consultas automatizables</div>
                  </div>
                  <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                    <div className="text-xl md:text-2xl font-bold text-green-600 mb-1">30-50%</div>
                    <div className="text-xs md:text-sm text-gray-600">Reducción carga CRM</div>
                  </div>
                  <div className="bg-white rounded-lg p-4 shadow-sm text-center">
                    <div className="text-xl md:text-2xl font-bold text-purple-600 mb-1">3-5 min</div>
                    <div className="text-xs md:text-sm text-gray-600">Ahorro por consulta</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;