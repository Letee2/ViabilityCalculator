import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def calcular_costes_almacenamiento_transferencia(num_videos, num_clientes, porcentaje_consumo, tipo_almacenamiento):
    """
    Calcula los costes de almacenamiento y transferencia según la fórmula especificada.
    
    Args:
        num_videos: Número de videos por fisio
        num_clientes: Número de clientes por fisio
        porcentaje_consumo: Porcentaje de videos que ve cada cliente
        tipo_almacenamiento: Tipo de almacenamiento en GCP
    """
    # Constantes
    tamanio_video_gb = 0.14  # 140 MB en GB
    tasa_conversion_usd_eur = 0.9
    
    # Tarifas GCP (USD -> EUR)
    tarifas_almacenamiento = {
        "Standard": 0.023 * tasa_conversion_usd_eur,
        "Nearline": 0.013 * tasa_conversion_usd_eur,
        "Coldline": 0.006 * tasa_conversion_usd_eur,
        "Archive": 0.0025 * tasa_conversion_usd_eur
    }
    tarifa_transferencia_gb = 0.02 * tasa_conversion_usd_eur

    # Cálculo del almacenamiento total por fisio
    almacenamiento_total_gb = num_videos * tamanio_video_gb
    
    # Coste de almacenamiento anual
    coste_almacenamiento_mensual = almacenamiento_total_gb * tarifas_almacenamiento[tipo_almacenamiento]
    coste_almacenamiento_anual = coste_almacenamiento_mensual * 12
    
    # Cálculo de transferencia
    gb_por_cliente = almacenamiento_total_gb * (porcentaje_consumo / 100)
    transferencia_mensual_gb = gb_por_cliente * num_clientes
    transferencia_anual_gb = transferencia_mensual_gb * 12
    coste_transferencia_anual = transferencia_anual_gb * tarifa_transferencia_gb
    
    return coste_almacenamiento_anual, coste_transferencia_anual, almacenamiento_total_gb, transferencia_anual_gb

def analizar_viabilidad(coste_total_5_anos, num_fisios, precio_plan_basico_mensual, precio_plan_premium_mensual, porcentaje_premium):
    """Analiza la viabilidad del proyecto con los precios dados y mix de planes."""
    # Calculamos el número de usuarios de cada tipo
    num_fisios_premium = int(num_fisios * (porcentaje_premium / 100))
    num_fisios_basico = num_fisios - num_fisios_premium
    
    # Calculamos ingresos anuales
    ingresos_basico_anual = num_fisios_basico * precio_plan_basico_mensual * 12
    ingresos_premium_anual = num_fisios_premium * precio_plan_premium_mensual * 12
    ingresos_total_anual = ingresos_basico_anual + ingresos_premium_anual
    
    # Calculamos ingresos a 5 años
    ingresos_5_anos = ingresos_total_anual * 5
    
    return {
        "es_viable": ingresos_5_anos >= coste_total_5_anos,
        "ingresos_5_anos": ingresos_5_anos,
        "deficit": coste_total_5_anos - ingresos_5_anos if ingresos_5_anos < coste_total_5_anos else 0,
        "desglose_anual": {
            "basico": ingresos_basico_anual,
            "premium": ingresos_premium_anual
        }
    }


def calcular_costes_y_precios(num_fisios=60, videos_por_fisio=15, clientes_por_fisio=10, coste_inicial=86487, 
                             porcentaje_consumo=70, tipo_almacenamiento="Standard",
                             coste_mantenimiento=15000, coste_soporte=10000, coste_hardware=5000,
                             precio_basico_mensual=2, precio_premium_mensual=4, porcentaje_premium=30):
    """Calcula los costes y precios recomendados para la app de fisios."""

    
    # Calcular costes de almacenamiento y transferencia
    coste_alm_anual, coste_trans_anual, almacenamiento_total, transferencia_total = \
        calcular_costes_almacenamiento_transferencia(
            videos_por_fisio, clientes_por_fisio, 
            porcentaje_consumo, tipo_almacenamiento
        )
    
    # Multiplicar por número de fisios
    coste_alm_total = coste_alm_anual * num_fisios
    coste_trans_total = coste_trans_anual * num_fisios
    
    # Costes operativos anuales
    costes_operativos = {
        "📂 Almacenamiento": coste_alm_total,
        "🔄 Transferencia": coste_trans_total,
        "🛠️ Mantenimiento": coste_mantenimiento,
        "📞 Soporte Técnico": coste_soporte,
        "💻 Hardware": coste_hardware
    }
    
    # Calcular coste total anual
    coste_total_anual = sum(costes_operativos.values())
    
    # Calcular coste total a 5 años (incluyendo coste inicial)
    coste_total_5_anos = (coste_total_anual * 5) + coste_inicial

    coste_alm_anual, coste_trans_anual, almacenamiento_total, transferencia_total = \
        calcular_costes_almacenamiento_transferencia(
            videos_por_fisio, clientes_por_fisio, 
            porcentaje_consumo, tipo_almacenamiento
        )
    
    coste_alm_total = coste_alm_anual * num_fisios
    coste_trans_total = coste_trans_anual * num_fisios
    
    costes_operativos = {
        "📂 Almacenamiento": coste_alm_total,
        "🔄 Transferencia": coste_trans_total,
        "🛠️ Mantenimiento": coste_mantenimiento,
        "📞 Soporte Técnico": coste_soporte,
        "💻 Hardware": coste_hardware
    }
    
    coste_total_anual = sum(costes_operativos.values())
    coste_total_5_anos = (coste_total_anual * 5) + coste_inicial

    # Análisis de viabilidad con el mix de precios
    viabilidad = analizar_viabilidad(coste_total_5_anos, num_fisios, 
                                   precio_basico_mensual, precio_premium_mensual,
                                   porcentaje_premium)

    return {
        "coste_total_anual": coste_total_anual,
        "coste_total_5_anos": coste_total_5_anos,
        "costes_desglosados": costes_operativos,
        "almacenamiento_total_gb": almacenamiento_total,
        "transferencia_total_gb": transferencia_total,
        "precio_basico_mensual": precio_basico_mensual,
        "precio_premium_mensual": precio_premium_mensual,
        "porcentaje_premium": porcentaje_premium,
        "viabilidad": viabilidad,
        "coste_por_fisio": {
            "📂 Almacenamiento": coste_alm_anual,
            "🔄 Transferencia": coste_trans_anual
        }
    }
def main():
    st.set_page_config(page_title="Estimación de Costes e Ingresos FisioFind", layout="wide")
    
    st.title("🧮 Estimación de Costes e Ingresos FisioFind")
    
    with st.sidebar:
        st.header("Parámetros de Entrada")
        
        # Parámetros principales
        st.subheader("Parámetros Principales")
        num_fisios = st.number_input("Número de fisios", 
                                   min_value=1, value=60,
                                   help="Cantidad total de fisioterapeutas usando la plataforma")
        
        videos_por_fisio = st.number_input("Videos por fisio",
                                         min_value=1, value=15,
                                         help="Cantidad de videos que publicará cada fisioterapeuta")
        
        clientes_por_fisio = st.number_input("Clientes por fisio", 
                                           min_value=1, value=10,
                                           help="Cantidad de clientes asociados a cada fisioterapeuta")
        
        coste_inicial = st.number_input("Coste inicial del proyecto (€)", 
                                      min_value=0, value=86487,
                                      help="Inversión inicial necesaria para el proyecto")
        
        # Configuración de precios
        st.subheader("Configuración de Precios")
        precio_basico_mensual = st.number_input("Precio Plan Básico (€/mes)",
                                              min_value=1.0, max_value=30.0, value=20.0,
                                              help="Precio mensual para el plan básico")
        
        precio_premium_mensual = st.number_input("Precio Plan Premium (€/mes)",
                                               min_value=precio_basico_mensual, max_value=60.0, value=35.0,
                                               help="Precio mensual para el plan premium")
        
        porcentaje_premium = st.slider("Porcentaje de usuarios Premium (%)", 
                                     min_value=0, max_value=50, value=30,
                                     help="Porcentaje de fisios que elegirán el plan premium")
        
        
        porcentaje_consumo = st.slider("Consumo de videos (%)", 
                                     min_value=0, max_value=100, value=70,
                                     help="Porcentaje de videos que verá cada cliente")
        
        # Costes operativos
        st.subheader("Costes Operativos Anuales")
        coste_mantenimiento = st.number_input("Coste de mantenimiento (€/año)",
                                            min_value=0, value=15000,
                                            help="Coste anual de mantenimiento y despliegue")
        
        coste_soporte = st.number_input("Coste de soporte técnico (€/año)",
                                       min_value=0, value=10000,
                                       help="Coste anual de atención al cliente")
        
        coste_hardware = st.number_input("Reserva para hardware (€/año)",
                                       min_value=0, value=5000,
                                       help="Reserva anual para reemplazo de hardware")
        
        # Configuración técnica
        st.subheader("Configuración Técnica")
        tipo_almacenamiento = st.selectbox("Tipo de almacenamiento en GCP",
                                         ["Standard", "Nearline", "Coldline", "Archive"],
                                         help="Tipo de almacenamiento en Google Cloud Platform")

    # Cálculos
    resultados = calcular_costes_y_precios(
        num_fisios, videos_por_fisio, clientes_por_fisio, coste_inicial,
        porcentaje_consumo, tipo_almacenamiento,
        coste_mantenimiento, coste_soporte, coste_hardware,
        precio_basico_mensual, precio_premium_mensual, porcentaje_premium
    )

    # El dashboard principal necesita actualizarse para mostrar el mix de planes
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Resumen de Costes")
        st.metric("Coste Total Anual", f"{resultados['coste_total_anual']:,.2f} €")
        st.metric("Coste Total a 5 años", f"{resultados['coste_total_5_anos']:,.2f} €")
        
        # Costes por fisio
        st.write("#### Costes por Fisio (Anual)")
        st.write(f"- Almacenamiento: {resultados['coste_por_fisio']['📂 Almacenamiento']:.2f} €")
        st.write(f"- Transferencia: {resultados['coste_por_fisio']['🔄 Transferencia']:.2f} €")
        
        # Gráfico de distribución de costes
        fig_pie, ax_pie = plt.subplots(figsize=(8, 6))
        costes = resultados['costes_desglosados']
        plt.pie(costes.values(), labels=costes.keys(), autopct='%1.1f%%', startangle=90)
        plt.title("Distribución de Costes Anuales")
        st.pyplot(fig_pie)
        
    with col2:
        st.subheader("💰 Análisis de Viabilidad (5 años)")
        
        num_fisios_premium = int(num_fisios * (porcentaje_premium / 100))
        num_fisios_basico = num_fisios - num_fisios_premium
        
        st.write("#### Distribución de Planes")
        st.write(f"- Plan Básico ({precio_basico_mensual} €/mes): **{num_fisios_basico}** fisios")
        st.write(f"- Plan Premium ({precio_premium_mensual} €/mes): **{num_fisios_premium}** fisios")
        
        if resultados['viabilidad']['es_viable']:
            st.success("✅ El modelo de negocio es viable")
            st.write(f"Ingresos a 5 años: {resultados['viabilidad']['ingresos_5_anos']:,.2f} €")
            st.write("#### Desglose de Ingresos Anuales")
            st.write(f"- Plan Básico: {resultados['viabilidad']['desglose_anual']['basico']:,.2f} €")
            st.write(f"- Plan Premium: {resultados['viabilidad']['desglose_anual']['premium']:,.2f} €")
        else:
            st.error(f"❌ El modelo no es viable. Déficit: {resultados['viabilidad']['deficit']:,.2f} €")
            
        # Punto de equilibrio con mix de planes
        st.write("#### Puntos de Equilibrio")
        
        # Calculamos el ingreso promedio por fisio al año considerando el mix
        ingreso_promedio_anual = (
            (precio_basico_mensual * 12 * (100 - porcentaje_premium) / 100) +
            (precio_premium_mensual * 12 * porcentaje_premium / 100)
        )
        
        equilibrio_total = max(1, int(np.ceil(resultados['coste_total_5_anos'] / (ingreso_promedio_anual * 5))))
        
        st.write(f"- **Total**: Se necesitan al menos **{equilibrio_total:,}** fisios")
        st.write(f"  - De los cuales **{int(equilibrio_total * porcentaje_premium / 100):,}** serían Premium")
        st.write(f"  - Y **{int(equilibrio_total * (100 - porcentaje_premium) / 100):,}** serían Básico")

        # Gráfico de uso de recursos
        fig_bar, ax_bar = plt.subplots(figsize=(8, 6))
        datos = pd.DataFrame({
            'Tipo': ['Almacenamiento', 'Transferencia'],
            'GB/año': [resultados['almacenamiento_total_gb'], 
                      resultados['transferencia_total_gb']]
        })
        sns.barplot(data=datos, x='Tipo', y='GB/año')
        plt.title("Uso Estimado de Recursos (GB/año)")
        plt.ylabel("Gigabytes")
        st.pyplot(fig_bar)

    # Detalles adicionales
    with st.expander("📝 Detalles del Cálculo"):
        st.write("### Costes Desglosados")
        for concepto, coste in resultados['costes_desglosados'].items():
            st.write(f"**{concepto}:** {coste:,.2f} €/año")
            
        st.write("\n### Análisis de Ingresos a 5 años")
        st.write(f"- Plan Básico ({precio_basico_mensual} €/mes): {resultados['viabilidad']['desglose_anual']['basico'] * 5:,.2f} €")
        st.write(f"- Plan Premium ({precio_premium_mensual} €/mes): {resultados['viabilidad']['desglose_anual']['premium'] * 5:,.2f} €")
        st.write(f"- **Total**: {resultados['viabilidad']['ingresos_5_anos']:,.2f} €")

if __name__ == "__main__":
    main()
