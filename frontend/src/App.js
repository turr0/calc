import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [formData, setFormData] = useState({
    monthly_inquiries: 1000,
    automation_percentage: 60,
    minutes_per_inquiry: 4,
    monthly_crm_hours: 40,
    crm_automation_percentage: 50,
    team_members: 3,
    hourly_cost_ars: 5000,
    bitrix24_annual_cost: 200000,
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

  const formatCurrency = (amount) => {
    if (!amount) return 'ARS $0';
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
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
                      Horas CRM mensuales
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
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
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
                      Licencia Bitrix24 anual (ARS)
                    </label>
                    <input
                      type="number"
                      name="bitrix24_annual_cost"
                      value={formData.bitrix24_annual_cost}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
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
                        {Math.round(results.total_annual_savings / results.total_investment * 12)}
                      </div>
                      <div className="text-sm text-gray-600">Meses para recuperar inversión</div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;