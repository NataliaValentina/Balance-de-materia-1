import streamlit as st

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Calculadora de Balance de Masa",
    page_icon="🍊",
    layout="wide"
)

# --- Título y Descripción ---
st.title("🍊 Calculadora de Balance de Masa para Pulpa de Fruta")
st.write("""
Esta aplicación resuelve un problema común de balance de materia en la industria de alimentos. 
El objetivo es calcular la cantidad de azúcar necesaria para ajustar la concentración de sólidos solubles (grados °Brix) 
de una pulpa de fruta a un valor deseado.
""")

# --- Columnas para la interfaz ---
col1, col2 = st.columns([1, 1.5])

with col1:
    # --- Entradas del Usuario con valores del ejemplo ---
    st.header("Parámetros de Entrada")
    st.write("Introduce los valores de tu proceso. Los valores iniciales corresponden al ejercicio de ejemplo.")

    # Usamos st.number_input para obtener valores numéricos
    m1 = st.number_input(
        label="Masa Inicial de Pulpa (M1) en kg:",
        min_value=0.0,
        value=50.0, # Valor del ejemplo
        step=1.0,
        help="Cantidad de pulpa que tienes al inicio del proceso."
    )

    x1 = st.number_input(
        label="Concentración Inicial de Sólidos (X1) en %Brix:",
        min_value=0.0,
        max_value=100.0,
        value=7.0, # Valor del ejemplo
        step=0.1,
        help="Porcentaje de sólidos solubles (azúcar) en la pulpa inicial."
    )

    x3 = st.number_input(
        label="Concentración Final Deseada (X3) en %Brix:",
        min_value=0.0,
        max_value=100.0,
        value=10.0, # Valor del ejemplo
        step=0.1,
        help="El porcentaje de °Brix que quieres alcanzar en el producto final."
    )
    
    # Parámetro del azúcar (generalmente es 100% sólidos)
    x2 = 100.0 

# --- Lógica de Cálculo ---
# Convertir porcentajes a fracción decimal para los cálculos
x1_frac = x1 / 100.0
x2_frac = x2 / 100.0
x3_frac = x3 / 100.0

# Inicializar variables de resultado
m2 = 0.0
m3 = 0.0
calculation_possible = False

# El denominador no puede ser cero (la concentración del azúcar debe ser mayor a la final)
if x2_frac > x3_frac:
    calculation_possible = True
    # Fórmula del balance de materia para sólidos: M1*X1 + M2*X2 = M3*X3
    # Sabiendo que M3 = M1 + M2, despejamos M2:
    # M2 = M1 * (X3 - X1) / (X2 - X3)
    m2 = m1 * (x3_frac - x1_frac) / (x2_frac - x3_frac)
    
    # Calculamos la masa final
    m3 = m1 + m2

with col2:
    # --- Resultados ---
    st.header("Resultados del Cálculo")
    
    if calculation_possible:
        st.success(f"Cálculo realizado con éxito.")
        
        # Mostrar resultados en métricas destacadas
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(
                label="➡️ Cantidad de Azúcar a Agregar (M2)",
                value=f"{m2:.2f} kg"
            )
        with res_col2:
            st.metric(
                label="✅ Masa de Pulpa Final (M3)",
                value=f"{m3:.2f} kg"
            )

        # --- Explicación del Proceso (Expansor) ---
        with st.expander("Ver el detalle de los cálculos"):
            st.write("El cálculo se basa en dos principios de conservación de la masa:")
            st.markdown("""
            1.  **Balance General de Masa:** La masa total que entra es igual a la que sale.
            2.  **Balance de Sólidos:** La masa de sólidos que entra es igual a la que sale.
            """)
            
            # Ecuaciones Generales en LaTeX
            st.subheader("Ecuaciones")
            st.latex(r"M_1 + M_2 = M_3")
            st.latex(r"M_1 \cdot X_1 + M_2 \cdot X_2 = M_3 \cdot X_3")
            
            st.write("Donde:")
            st.markdown(f"""
            - $M_1$ (Masa Inicial) = **{m1} kg**
            - $X_1$ (Concentración Inicial) = **{x1}%**
            - $M_2$ (Masa de Azúcar) = **? kg**
            - $X_2$ (Concentración de Azúcar) = **{x2}%**
            - $M_3$ (Masa Final) = **? kg**
            - $X_3$ (Concentración Final) = **{x3}%**
            """)

            # Desglose del cálculo con los valores del usuario
            st.subheader("Paso a Paso")
            st.write("1. Despejamos la masa de azúcar a agregar (M2) de las ecuaciones:")
            st.latex(r"M_2 = \frac{M_1 \cdot (X_3 - X_1)}{X_2 - X_3}")
            
            st.write("2. Sustituimos los valores (en formato decimal):")
            st.latex(fr"M_2 = \frac{{{m1} \cdot ({x3_frac} - {x1_frac})}}{{{x2_frac} - {x3_frac}}} = \frac{{{m1 * (x3_frac - x1_frac):.2f}}}{{{x2_frac - x3_frac}}} \approx {m2:.2f} \text{{ kg}}")
            
            st.write("3. Calculamos la masa final (M3):")
            st.latex(fr"M_3 = M_1 + M_2 = {m1} + {m2:.2f} = {m3:.2f} \text{{ kg}}")
            
    else:
        st.error("Error en los datos de entrada: La concentración final deseada debe ser menor que la concentración del azúcar añadido (100%).")

# --- Pie de Página ---
st.markdown("---")

st.markdown("Creado con ❤️ por [Natalia Valentina] usando [Streamlit](https://streamlit.io).")
