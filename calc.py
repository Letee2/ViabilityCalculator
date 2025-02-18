import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random


# -------------------------------------------------
# FUNCIONES DE CÁLCULO
# -------------------------------------------------

def calcular_costes_desarrollo(usar_horas_reales=False, horas_reales=None):
    """
    Calcula los costes de desarrollo iniciales basados en el equipo y horas.
    Permite comparar entre horas estimadas y reales, y devuelve un desglose
    mensual más detallado.
    """
    # Costes por hora (fijos)
    costes_hora = {
        "desarrollador": 27,
        "analista": 30.82,
        "pm": 37.25
    }
    
    # Estructura del equipo (fija)
    equipo = {
        "desarrollador": 11,
        "analista": 5,
        "pm": 1
    }
    
    # Horas estimadas por mes (ya incluyen un 20% de incremento)
    horas_estimadas = {
        "febrero": 36,
        "marzo": 48,
        "abril": 36,
        "mayo": 36
    }
    
    # Elegir las horas a usar (estimadas o reales)
    horas_mes = horas_reales if (usar_horas_reales and horas_reales) else horas_estimadas
    
    # Costes fijos mensuales (hardware, GitHub y preproducción)
    costes_fijos = {
        "hardware": 440,        # Coste mensual derivado de la renovación de equipos
        "github": 340.68,       # 20,04€ x 17 personas
        "preproduccion": 20     # Entornos de preproducción
    }
    
    # Calcular los costes mensuales y preparar un desglose más detallado
    desglose_detallado = []
    costes_mensuales_totales = {}  # Para almacenar el total de cada mes
    
    for mes, horas in horas_mes.items():
        # Coste personal en función de las horas y roles
        coste_personal = sum(
            costes_hora[rol] * num * horas 
            for rol, num in equipo.items()
        )
        
        # Desglose de costes fijos
        coste_hardware = costes_fijos["hardware"]
        coste_github = costes_fijos["github"]
        coste_preprod = costes_fijos["preproduccion"]
        
        # Subtotal = costes de personal + costes fijos
        subtotal = coste_personal + coste_hardware + coste_github + coste_preprod
        
        # Contingencia 10% sobre subtotal
        contingencia = subtotal * 0.1
        
        # Total del mes
        total_mes = subtotal + contingencia
        
        # Se almacena en una lista que nos permita mostrar un dataframe
        desglose_detallado.append({
            "Mes": mes.capitalize(),
            "Coste Personal": coste_personal,
            "Hardware": coste_hardware,
            "GitHub": coste_github,
            "Preproducción": coste_preprod,
            "Subtotal": subtotal,
            "Contingencia (10%)": contingencia,
            "Total Mes": total_mes
        })
        
        costes_mensuales_totales[mes] = total_mes
    
    coste_total_desarrollo = sum(costes_mensuales_totales.values())
    
    return {
        "costes_mensuales": costes_mensuales_totales,
        "coste_total": coste_total_desarrollo,
        "desglose_equipo": equipo,
        "costes_hora": costes_hora,
        "horas_mes": horas_mes,
        "costes_fijos": costes_fijos,
        "desglose_detallado": desglose_detallado  # Lista con el breakdown de cada mes
    }

def mostrar_tabla_comparativa(horas_estimadas, horas_reales):
    """
    Muestra una tabla comparativa de horas estimadas vs reales.
    Retorna un DataFrame con la diferencia.
    """
    df_comparacion = pd.DataFrame({
        'Mes': horas_estimadas.keys(),
        'Horas Estimadas': horas_estimadas.values(),
        'Horas Reales': [horas_reales.get(mes, 0) for mes in horas_estimadas.keys()],
        'Diferencia': [
            horas_reales.get(mes, 0) - horas_estimadas[mes] 
            for mes in horas_estimadas.keys()
        ]
    })
    return df_comparacion



def generar_crecimiento_aleatorio(inicial, final, num_meses, ruido_factor=0.1, prob_perdida=0.15, max_perdida=0.05):
    """
    Genera una serie de valores con una tendencia global de crecimiento
    desde 'inicial' hasta 'final', pero con fluctuaciones realistas.

    - `ruido_factor`: Magnitud del ruido (fluctuaciones naturales).
    - `prob_perdida`: Probabilidad (0-1) de que un mes haya una caída en el número de fisios.
    - `max_perdida`: Máxima reducción posible en un mes si ocurre una caída.
    """
    if num_meses <= 1:
        return [final] * num_meses

    valores = []
    valor_actual = float(inicial)
    paso = (final - inicial) / (num_meses - 1) if num_meses > 1 else 0

    for i in range(num_meses):
        # Factor aleatorio de ruido (pequeñas variaciones)
        ruido = random.uniform(-ruido_factor, ruido_factor) * paso
        
        # Determinar si hay una caída de fisios este mes
        if random.random() < prob_perdida:
            perdida = random.uniform(0, max_perdida) * valor_actual  # Hasta un % del total actual
            valor_actual -= perdida
        else:
            # Crecimiento con fluctuaciones
            valor_actual += paso + ruido

        # No permitir valores negativos
        if valor_actual < 0:
            valor_actual = 0
        
        valor_actual = round(valor_actual)
        valores.append(int(valor_actual))
    
    return valores
def calcular_costes_almacenamiento_transferencia(
    num_videos, 
    num_clientes, 
    porcentaje_consumo, 
    tipo_almacenamiento
):
    """
    Calcula los costes de almacenamiento y transferencia según la fórmula especificada.
    """
    tamanio_video_gb = 0.14  # 140 MB -> 0.14 GB
    tasa_conversion_usd_eur = 0.9
    
    # Tarifas GCP (USD -> EUR)
    tarifas_almacenamiento = {
        "Standard": 0.023 * tasa_conversion_usd_eur,
        "Nearline": 0.013 * tasa_conversion_usd_eur,
        "Coldline": 0.006 * tasa_conversion_usd_eur,
        "Archive": 0.0025 * tasa_conversion_usd_eur
    }
    tarifa_transferencia_gb = 0.02 * tasa_conversion_usd_eur

    # Almacenamiento total (GB) de un fisio
    almacenamiento_total_gb = num_videos * tamanio_video_gb

    # Coste almacenamiento anual (1 fisio)
    coste_alm_mensual = almacenamiento_total_gb * tarifas_almacenamiento[tipo_almacenamiento]
    coste_alm_anual = coste_alm_mensual * 12

    # Transferencia anual
    gb_por_cliente = almacenamiento_total_gb * (porcentaje_consumo / 100.0)
    transferencia_mensual_gb = gb_por_cliente * num_clientes
    transferencia_anual_gb = transferencia_mensual_gb * 12
    coste_transferencia_anual = transferencia_anual_gb * tarifa_transferencia_gb
    
    return coste_alm_anual, coste_transferencia_anual, almacenamiento_total_gb, transferencia_anual_gb

def coste_operacion_mensual(
    mes_num,
    # Mantenimiento
    incidencias_iniciales,
    decremento_incidencias,
    modo_mantenimiento_adaptativo,
    # Chatbot
    chatbot_plan,
    coste_apis_mensual,
    # Par. del mes
    fisios_actual,
    videos_por_fisio_promedio,
    clientes_actual,
    porcentaje_consumo,
    tipo_almacenamiento
):
    """Calcula el coste de operación para un mes, dados los parámetros."""
    # 1) Chatbot
    if chatbot_plan == "plan1":
        coste_chatbot = 425.51
    else:
        coste_chatbot = 74.0  # ~79 USD -> 74€

    # 2) Mantenimiento adaptativo
    # 2 jornadas * 8h * 27€/h => 432€ trimestral => 1728€/año
    def mantenimiento_adapt(m):
        if modo_mantenimiento_adaptativo == "prorrateado":
            return 1728 / 12.0  # 144 €/mes
        else:
            # Solo en meses 3,6,9,12 => 432€, resto 0
            if m % 3 == 0:
                return 432
            else:
                return 0

    coste_adaptativo = mantenimiento_adapt(mes_num)

    # 3) Mantenimiento correctivo
    incidencias_mes = max(1, incidencias_iniciales - (mes_num - 1)*decremento_incidencias)
    coste_correctivo = incidencias_mes * 27

    # 4) Almacenamiento y transferencia
    coste_alm_anual_1, coste_trans_anual_1, _, _ = calcular_costes_almacenamiento_transferencia(
        videos_por_fisio_promedio,
        clientes_actual,
        porcentaje_consumo,
        tipo_almacenamiento
    )
    # multiplica por fisios_actual y divide entre 12 para tener mensual
    coste_alm_mensual = (coste_alm_anual_1 * fisios_actual) / 12.0
    coste_trans_mensual = (coste_trans_anual_1 * fisios_actual) / 12.0

    # 5) Otros costes
    coste_despliegue = 60

    # 6) Total
    total_mes = (
        coste_chatbot +
        coste_despliegue +
        coste_correctivo +
        coste_adaptativo +
        coste_apis_mensual +
        coste_alm_mensual +
        coste_trans_mensual
    )

    return {
        "Mes": mes_num,
        "Fisios": fisios_actual,
        "Clientes/fisio": clientes_actual,
        "Videos/fisio (avg)": videos_por_fisio_promedio,
        "Chatbot": coste_chatbot,
        "Despliegue": coste_despliegue,
        "Mantenimiento Correctivo": coste_correctivo,
        "Mantenimiento Adaptativo": coste_adaptativo,
        "APIs": coste_apis_mensual,
        "Almacenamiento (GCP)": coste_alm_mensual,
        "Transferencia (GCP)": coste_trans_mensual,
        "Total Mensual": total_mes
    }

def calcular_costes_operacion_simulacion(
    fisios_inicial,
    fisios_final,
    clientes_inicial,
    clientes_final,
    basic_videos,
    premium_videos,
    porcentaje_premium,
    porcentaje_consumo,
    tipo_almacenamiento,
    # Mantenimiento
    incidencias_iniciales,
    decremento_incidencias,
    modo_mantenimiento_adaptativo,
    # Chatbot
    chatbot_plan,
    coste_apis_anual,
    # Simulación
    num_meses,
    # Factor de ruido
    ruido_factor=0.1
):
    """
    Simula los costes de operación mes a mes, usando un 'crecimiento' aleatorio 
    con tendencia, y diferenciando vídeos básicos/premium.
    """
    # Generamos la secuencia de fisios y clientes con factor aleatorio
    fisios_por_mes = generar_crecimiento_aleatorio(fisios_inicial, fisios_final, num_meses, ruido_factor)
    clientes_por_mes = generar_crecimiento_aleatorio(clientes_inicial, clientes_final, num_meses, ruido_factor)

    # Coste de APIs prorrateado
    coste_apis_mensual = coste_apis_anual / 12.0

    # Para cada mes, calculamos la media ponderada de vídeos/fisio
    filas = []
    for i in range(num_meses):
        mes_num = i + 1
        fisios_act = fisios_por_mes[i]
        clientes_act = clientes_por_mes[i]

        if fisios_act <= 0:
            videos_promedio = 0
        else:
            # # fisios premium
            premium_f = fisios_act * (porcentaje_premium / 100.0)
            basic_f = fisios_act - premium_f
            videos_promedio = (premium_f * premium_videos + basic_f * basic_videos) / fisios_act

        fila_mes = coste_operacion_mensual(
            mes_num=mes_num,
            incidencias_iniciales=incidencias_iniciales,
            decremento_incidencias=decremento_incidencias,
            modo_mantenimiento_adaptativo=modo_mantenimiento_adaptativo,
            chatbot_plan=chatbot_plan,
            coste_apis_mensual=coste_apis_mensual,
            fisios_actual=fisios_act,
            videos_por_fisio_promedio=videos_promedio,
            clientes_actual=clientes_act,
            porcentaje_consumo=porcentaje_consumo,
            tipo_almacenamiento=tipo_almacenamiento
        )
        filas.append(fila_mes)

    df_resultado = pd.DataFrame(filas)
    return df_resultado


def mostrar_pestana_costes_operacion():
    st.title("Costes de Operación")

    # 1) Crecimiento de Fisios y Clientes
    st.subheader("1) Crecimiento de Fisios y Clientes")
    st.info("""
    En esta sección definimos cuántos fisioterapeutas y cuántos clientes 
    por fisio tenemos al inicio (Mes 1) y cuánto esperamos alcanzar 
    al final del período (Mes N). 

    **Nota**: Hemos introducido un factor aleatorio para simular 
    fluctuaciones reales (p.ej., bajas puntuales), manteniendo una 
    tendencia general de crecimiento.
    """)
    col1, col2 = st.columns(2)
    with col1:
        fisios_inicial = st.number_input("Fisios - Valor inicial", min_value=0, max_value=100000, value=100)
        fisios_final = st.number_input("Fisios - Valor final", min_value=0, max_value=200000, value=700)
    with col2:
        clientes_inicial = st.number_input("Clientes/fisio - Valor inicial", min_value=0, max_value=50000, value=10)
        clientes_final = st.number_input("Clientes/fisio - Valor final", min_value=0, max_value=200000, value=30)

    # 2) Parámetros de Vídeos
    st.subheader("2) Parámetros de Vídeos")
    st.info("""
    Definimos cuántos vídeos puede subir un fisio **Básico** 
    vs. un fisio **Premium**. El porcentaje de fisios premium 
    determinará la media ponderada de vídeos por profesional.
    """)
    col3, col4 = st.columns(2)
    with col3:
        basic_videos = st.number_input("Vídeos por Fisio (Básico)", 1, 500, 10)
        premium_videos = st.number_input("Vídeos por Fisio (Premium)", 1, 500, 15)
    with col4:
        porcentaje_premium = st.slider("Porcentaje Fisios Premium (%)", 0, 100, 30)
        porcentaje_consumo = st.slider("Porcentaje de consumo de vídeos (%)", 0, 100, 70)

    tipo_almacenamiento = st.selectbox("Tipo de almacenamiento GCP", ["Standard", "Nearline", "Coldline", "Archive"])

    # 3) Costes Chatbot y APIs
    st.subheader("3) Costes Chatbot y APIs")
    plan_chatbot = st.radio("Plan de Chatbot", ["Plan 1 (425,51 €/mes)", "Plan 2 (74 €/mes)"])
    if "74" in plan_chatbot:
        chatbot_plan = "plan2"
    else:
        chatbot_plan = "plan1"

    coste_apis_anual = st.number_input("Coste APIs anual (€)", 100, 100000, 1500)

    # 4) Mantenimiento
    st.subheader("4) Mantenimiento")
    with st.expander("Detalles de Mantenimiento", expanded=False):
        st.markdown("""
        **Mantenimiento Adaptativo**:
        - Revisiones trimestrales (2 jornadas x 8h x 27€/h = 432€).
        - Puede prorratearse (144€/mes) o cargarse solo en meses 3, 6, 9, 12.

        **Mantenimiento Correctivo**:
        - Incidencias estimadas en el primer mes, que decrecen mensualmente con un tope de 1.
        - Cada incidencia = 1h x 27€/h = 27€.
        """)
    col5, col6 = st.columns(2)
    with col5:
        incidencias_iniciales = st.number_input("Incidencias iniciales (mes 1)", 0, 100, 10)
        decremento_incidencias = st.number_input("Decremento incidencias/mes", 0, 10, 1)
    with col6:
        modo_mantenimiento_adaptativo = st.selectbox("Mantenimiento Adaptativo", ["prorrateado", "trimestral"])

    # 5) Meses de análisis
    st.subheader("5) Meses de Análisis")
    num_meses = st.slider("Duración (meses)", 1, 60, 24)

    # Factor de ruido
    ruido_factor = st.slider("Factor de fluctuación aleatoria", 0.0, 0.5, 0.3, 0.05)

    # Botón para recalcular (cada vez que se hace clic, se generan nuevas fluctuaciones)
    if st.button("Generar Desglose"):
        df_result = calcular_costes_operacion_simulacion(
            fisios_inicial=fisios_inicial,
            fisios_final=fisios_final,
            clientes_inicial=clientes_inicial,
            clientes_final=clientes_final,
            basic_videos=basic_videos,
            premium_videos=premium_videos,
            porcentaje_premium=porcentaje_premium,
            porcentaje_consumo=porcentaje_consumo,
            tipo_almacenamiento=tipo_almacenamiento,
            incidencias_iniciales=incidencias_iniciales,
            decremento_incidencias=decremento_incidencias,
            modo_mantenimiento_adaptativo=modo_mantenimiento_adaptativo,
            chatbot_plan=chatbot_plan,
            coste_apis_anual=coste_apis_anual,
            num_meses=num_meses,
            ruido_factor=ruido_factor
        )

        # 6) Mostrar tabla
        st.subheader("Desglose Mensual de Costes")
        df_display = df_result.copy()
        # 1) Ver qué columnas tiene el DataFrame antes de aplicar cambios

        # 2) Verificar si el DataFrame está vacío
        if df_display.empty:
            st.error("El DataFrame está vacío. Revisa si los datos se generaron correctamente.")
            return

        # 3) Aplicar formateo solo a columnas que existen
        cols_monetarias = [
            "Chatbot", "Despliegue", "Mantenimiento Correctivo",
            "Mantenimiento Adaptativo", "APIs", "Almacenamiento (GCP)",
            "Transferencia (GCP)", "Total Mensual"
        ]

        for c in cols_monetarias:
            if c in df_display.columns:
                df_display[c] = df_display[c].apply(lambda x: f"{x:,.2f} €")
            else:
                st.warning(f"La columna '{c}' no se encuentra en el DataFrame.")


        st.dataframe(df_display)

        # Métrica de coste total
        coste_total = df_result["Total Mensual"].sum()
        st.session_state["df_operacion"] = df_display
        st.info(f"**Coste Total del Período:** {coste_total:,.2f} €")


    else:
        st.warning("Haz clic en 'Generar Desglose' para ver el resultado.")



# -------------------------------------------------
# SECCION ROI
# -------------------------------------------------
def mostrar_pestana_proyeccion_y_roi():
    st.header("Proyección de Ingresos y ROI")
    
    # 1. Recuperar datos de la sesión
    coste_desarrollo = st.session_state.get("coste_desarrollo")
    df_operacion = st.session_state.get("df_operacion")
    
    if coste_desarrollo is None or df_operacion is None:
        st.error("⚠️ Necesitas completar las secciones anteriores primero")
        return

    # 2. Convertir la columna "Total Mensual" a numérica
    df_operacion_num = df_operacion.copy()
    columnas_monetarias = [
        "Chatbot", "Despliegue", "Mantenimiento Correctivo",
        "Mantenimiento Adaptativo", "APIs", "Almacenamiento (GCP)",
        "Transferencia (GCP)", "Total Mensual"
    ]
    
    for col in columnas_monetarias:
        if col in df_operacion_num.columns:
            df_operacion_num[col] = df_operacion_num[col].apply(
                lambda x: float(str(x).replace('€', '').replace(',', '').strip())
                if isinstance(x, str) else x
            )

    # 3. Mostrar métricas iniciales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "💰 Inversión Inicial",
            f"{coste_desarrollo:,.2f}€",
            help="Coste total del desarrollo inicial"
        )
    with col2:
        coste_mensual_promedio = df_operacion_num["Total Mensual"].mean()
        st.metric(
            "⚙️ Coste Operativo Mensual Promedio",
            f"{coste_mensual_promedio:,.2f}€",
            help="Promedio de costes mensuales de operación"
        )
    with col3:
        coste_anual = coste_mensual_promedio * 12
        st.metric(
            "📅 Coste Operativo Anual",
            f"{coste_anual:,.2f}€",
            help="Proyección del coste operativo anual"
        )
    with col4:
        num_meses = len(df_operacion_num)
        st.metric(
            "📅 Período de Análisis",
            f"{num_meses} meses",
            help="Número de meses en la proyección"
        )

    # 4. Configuración de precios
    st.subheader("🏷️ Configuración de Precios")
    col1, col2 = st.columns(2)
    with col1:
        precio_standard = st.number_input(
            "Precio Plan Standard (€/mes)",
            min_value=0.0,
            max_value=100.0,
            value=17.99,
            step=0.5,
            format="%.2f"
        )
    with col2:
        precio_premium = st.number_input(
            "Precio Plan Premium (€/mes)",
            min_value=0.0,
            max_value=100.0,
            value=24.99,
            step=0.5,
            format="%.2f"
        )

    # 5. Cálculo de ingresos y ROI
    st.subheader("📊 Análisis de ROI")
    
    porcentaje_premium = st.slider(
        "Porcentaje de Fisios Premium",
        0, 100, 30,
        help="Porcentaje de fisioterapeutas que eligen el plan Premium"
    )

    # Usar el DataFrame con valores numéricos para los cálculos
    df_roi = df_operacion_num.copy()
    df_roi["Fisios Premium"] = df_roi["Fisios"] * (porcentaje_premium / 100.0)
    df_roi["Fisios Standard"] = df_roi["Fisios"] - df_roi["Fisios Premium"]
    df_roi["Ingresos Mensuales"] = (
        df_roi["Fisios Standard"] * precio_standard +
        df_roi["Fisios Premium"] * precio_premium
    )

    # Calculamos costes e ingresos acumulados
    df_roi["Costes Acumulados"] = coste_desarrollo + df_roi["Total Mensual"].cumsum()
    df_roi["Ingresos Acumulados"] = df_roi["Ingresos Mensuales"].cumsum()
    df_roi["ROI"] = df_roi["Ingresos Acumulados"] - df_roi["Costes Acumulados"]

    # 6. Punto de equilibrio y análisis
    break_even_month = None
    for idx, row in df_roi.iterrows():
        if row["ROI"] >= 0:
            break_even_month = row["Mes"]
            break

    if break_even_month:
        st.success(f"🎯 Punto de equilibrio alcanzado en el mes {int(break_even_month)}")
    else:
        # Calcular fisios necesarios para punto de equilibrio
        ultimo_mes = df_roi.iloc[-1]
        costes_mensuales = ultimo_mes["Total Mensual"]
        precio_promedio = (precio_standard * (1 - porcentaje_premium/100) + 
                         precio_premium * (porcentaje_premium/100))
        
        fisios_necesarios = (costes_mensuales + (coste_desarrollo / num_meses)) / precio_promedio
        fisios_actuales = ultimo_mes["Fisios"]
        
        incremento_precio_necesario = ((costes_mensuales + (coste_desarrollo / num_meses)) / 
                                     fisios_actuales) - precio_promedio
        
        st.warning(
            f"⚠️ No se alcanza el punto de equilibrio en el período analizado. "
            f"Para alcanzarlo necesitarías:\n\n"
            f"- Aumentar a {fisios_necesarios:.0f} fisios (actualmente {fisios_actuales:.0f}) o\n"
            f"- Incrementar el precio promedio en {incremento_precio_necesario:.2f}€ "
            f"(actualmente {precio_promedio:.2f}€)"
        )

    # Resto del código igual...
    # 7. Gráficas
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(df_roi["Mes"], df_roi["Ingresos Acumulados"], 
             label="Ingresos Acumulados", marker='o')
    ax1.plot(df_roi["Mes"], df_roi["Costes Acumulados"], 
             label="Costes Acumulados", marker='o')
    ax1.plot(df_roi["Mes"], df_roi["ROI"], 
             label="ROI", marker='o')
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.3)
    ax1.set_xlabel("Mes")
    ax1.set_ylabel("Euros")
    ax1.set_title("Evolución de Ingresos, Costes y ROI")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    st.pyplot(fig1)

    # 8. Tabla de resultados
    st.subheader("📑 Desglose Mensual Detallado")
    df_display = df_roi.copy()
    columnas_formato = [
        "Ingresos Mensuales", "Total Mensual", "Costes Acumulados",
        "Ingresos Acumulados", "ROI"
    ]
    for col in columnas_formato:
        df_display[col] = df_display[col].apply(lambda x: f"{x:,.2f}€")
    st.dataframe(df_display)

    # 9. Métricas finales
    st.subheader("📈 Métricas Clave")
    col1, col2, col3 = st.columns(3)
    with col1:
        roi_final = df_roi["ROI"].iloc[-1]
        st.metric(
            "ROI Final",
            f"{roi_final:,.2f}€",
            delta=f"{(roi_final/coste_desarrollo*100):,.1f}%" if roi_final > 0 else None
        )
    with col2:
        ingresos_ultimo_mes = df_roi["Ingresos Mensuales"].iloc[-1]
        st.metric(
            "Ingresos Último Mes",
            f"{ingresos_ultimo_mes:,.2f}€"
        )
    with col3:
        margen_ultimo_mes = ingresos_ultimo_mes - df_roi["Total Mensual"].iloc[-1]
        st.metric(
            "Margen Último Mes",
            f"{margen_ultimo_mes:,.2f}€",
            delta=f"{(margen_ultimo_mes/ingresos_ultimo_mes*100):,.1f}%"
        )
    st.subheader("📜 Reporte Detallado")
    coste_total_operacion = df_roi["Total Mensual"].sum()  # Suma de todos los costes mensuales (sin acumular dev)
    st.markdown(f"""
- **Coste de Desarrollo (inversión inicial):** {coste_desarrollo:,.2f}€
- **Coste de Operación total (período analizado):** {coste_total_operacion:,.2f}€
- **ROI final:** {roi_final:,.2f}€
- **Punto de equilibrio:** {'Mes ' + str(int(break_even_month)) if break_even_month else 'No alcanzado'}
- **Resumen**:
  - Este reporte muestra la suma de **Costes de Desarrollo** y el **Coste Operativo** mes a mes, 
  - comparándolo con los **Ingresos Mensuales** calculados a partir de la configuración actual de precios.
""")

# -------------------------------------------------
# APLICACIÓN PRINCIPAL (STREAMLIT)
# -------------------------------------------------

def main():
    st.set_page_config(page_title="FisioFind - Análisis de Costes", layout="wide")
    st.title("📊 Análisis de Costes y ROI - FisioFind")

    # Pestañas
    tab1, tab2, tab3 = st.tabs([
        "💰 Costes Iniciales",
        "⚙️ Costes de Operación",
        "📈 Proyección y ROI"
    ])
    
    # -----------------------------
    # PESTAÑA 1: Costes Iniciales
    # -----------------------------
    with tab1:
        st.header("Costes de Desarrollo Inicial")
        
        # Mostrar información del equipo y costes base
        st.subheader("📋 Configuración Base del Proyecto")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("#### 👥 Composición del Equipo")
            st.markdown("""
            - 11 Desarrolladores Fullstack
            - 5 Analistas
            - 1 Project Manager
            """)
            
            st.write("#### 💶 Costes por Hora")
            st.markdown("""
            - Desarrollador: 27€/hora
            - Analista: 30.82€/hora
            - Project Manager: 37.25€/hora
            """)
        
        with col2:
            st.write("#### ⏱️ Horas Estimadas por Mes")
            st.markdown("""
            - Febrero: 36 horas
            - Marzo: 48 horas
            - Abril: 36 horas
            - Mayo: 36 horas
            """)
            
            st.write("#### 💡 Justificación de Horas")
            st.info("""
            Las horas estimadas incluyen un incremento del 20% sobre la base inicial 
            para cubrir posibles desviaciones y trabajo adicional no previsto:
            - Meses estándar: 30h + 20% = 36h
            - Marzo (mes intensivo): 40h + 20% = 48h
            """)
        
        # Separador visual
        st.divider()
        
        # Sección de horas reales
        st.subheader("📊 Seguimiento de Horas Reales")
        st.markdown("""
        Esta sección permite introducir las horas reales trabajadas por el equipo para 
        comparar con la estimación inicial y calcular las desviaciones en costes.
        """)

        # Selector de modo de cálculo
        modo_calculo = st.radio(
            "Modo de cálculo",
            ["Usar horas estimadas", "Usar horas reales"],
            horizontal=True
        )
        
        # Inicializamos variable de resultados del cálculo
        resultados_desarrollo = {}
        
        if modo_calculo == "Usar horas reales":
            col1, col2 = st.columns(2)
            
            with col1:
                # Input de horas reales
                horas_reales = {}
                for mes in ["febrero", "marzo", "abril", "mayo"]:
                    horas_reales[mes] = st.number_input(
                        f"Horas reales {mes.capitalize()}",
                        min_value=0,
                        max_value=100,
                        value=36
                    )
                
                # Calcular con horas reales
                resultados_desarrollo = calcular_costes_desarrollo(
                    usar_horas_reales=True,
                    horas_reales=horas_reales
                )
            
            with col2:
                # Mostrar comparativa entre estimadas y reales
                df_comp = mostrar_tabla_comparativa(
                    calcular_costes_desarrollo(usar_horas_reales=False)['horas_mes'],
                    horas_reales
                )
                st.write("#### Comparativa de Horas")
                st.dataframe(df_comp.style.background_gradient(subset=['Diferencia'], cmap='RdYlGn'))
        
        else:
            # Usar horas estimadas
            resultados_desarrollo = calcular_costes_desarrollo(
                usar_horas_reales=False, 
                horas_reales=None
            )
        
        # Mostrar resultados de costes
        st.divider()
        
        # Sección de desglose mensual detallado
        st.write("### Desglose por Mes (Costes de Desarrollo)")
        df_desglose = pd.DataFrame(resultados_desarrollo["desglose_detallado"])
        # Ajustamos formato de columnas numéricas a dos decimales
        for col in df_desglose.columns:
            if col not in ["Mes"]:
                df_desglose[col] = df_desglose[col].apply(lambda x: f"{x:,.2f} €")
        
        st.table(df_desglose)
        
        # Métrica total del desarrollo
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Coste Total de Desarrollo",
                f"{resultados_desarrollo['coste_total']:,.2f}€"
            )
        
        # Gráfico de barras con el total mensual
        with col2:
            fig, ax = plt.subplots(figsize=(8, 4))
            meses = list(resultados_desarrollo['costes_mensuales'].keys())
            costes_totales = list(resultados_desarrollo['costes_mensuales'].values())
            
            bars = plt.bar(meses, costes_totales, color='royalblue')
            plt.title("Costes de Desarrollo por Mes")
            plt.xticks(rotation=45)
            plt.ylabel("Euros")
            
            # Añadir etiquetas de valor sobre las barras
            for bar in bars:
                height = bar.get_height()
                plt.text(
                    bar.get_x() + bar.get_width()/2.,
                    height,
                    f'{height:,.0f}€',
                    ha='center', 
                    va='bottom'
                )
            
            st.pyplot(fig)
        
        # Guardamos en sesión el coste de desarrollo para utilizarlo en la pestaña de ROI
        st.session_state["coste_desarrollo"] = resultados_desarrollo["coste_total"]
    

    # -----------------------------
    # PESTAÑA 2: Costes de Operación
    # -----------------------------
    with tab2:

        mostrar_pestana_costes_operacion()

    # Gráfico de barras del coste total mensual
   
    
    # -----------------------------
    # PESTAÑA 3: Proyección y ROI
    # -----------------------------
    with tab3:
        mostrar_pestana_proyeccion_y_roi()

# -------------------------------------------------
# EJECUCIÓN
# -------------------------------------------------
if __name__ == "__main__":
    main()

