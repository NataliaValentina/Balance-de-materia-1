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
        value=50.0,
        step=1.0,
        help="Cantidad de pulpa que tienes al inicio del proceso."
    )

    x1 = st.number_input(
        label="Concentración Inicial de Sólidos (X1) en %Brix:",
        min_value=0.0,
        max_value=100.0,
        value=7.0,
        step=0.1,
        help="Porcentaje de sólidos solubles (azúcar) en la pulpa inicial."
    )

    x3 = st.number_input(
        label="Concentración Final Deseada (X3) en %Brix:",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.1,
        help="El porcentaje de °Brix que quieres alcanzar en el producto final."
    )
    
    # Parámetro del azúcar (generalmente es 100% sólidos)
    x2 = 100.0 

    # --- CAMBIO: Se agrega un botón para iniciar el cálculo ---
    calculate_button = st.button("Calcular Balance", type="primary")

with col2:
    st.header("Resultados del Cálculo")
    
    # --- CAMBIO: La lógica de cálculo y los resultados ahora solo se ejecutan si se presiona el botón ---
    if calculate_button:
        # --- Lógica de Cálculo ---
        # Convertir porcentajes a fracción decimal para los cálculos
        x1_frac = x1 / 100.0
        x2_frac = x2 / 100.0
        x3_frac = x3 / 100.0

        # El denominador no puede ser cero (la concentración del azúcar debe ser mayor a la final)
        if x2_frac > x3_frac:
            # Fórmula del balance de materia para sólidos: M1*X1 + M2*X2 = M3*X3
            # Sabiendo que M3 = M1 + M2, despejamos M2:
            # M2 = M1 * (X3 - X1) / (X2 - X3)
            m2 = m1 * (x3_frac - x1_frac) / (x2_frac - x3_frac)
            
            # Calculamos la masa final
            m3 = m1 + m2

            # --- Resultados ---
            st.success(f"Cálculo realizado con éxito.")
            
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
                st.subheader("Ecuaciones")
                st.latex(r"M_1 + M_2 = M_3")
                st.latex(r"M_1 \cdot X_1 + M_2 \cdot X_2 = M_3 \cdot X_3")
                st.subheader("Paso a Paso con tus datos")
                st.latex(r"M_2 = \frac{M_1 \cdot (X_3 - X_1)}{X_2 - X_3}")
                st.latex(fr"M_2 = \frac{{{m1} \cdot ({x3_frac} - {x1_frac})}}{{{x2_frac} - {x3_frac}}} \approx {m2:.2f} \text{{ kg}}")
                st.latex(fr"M_3 = M_1 + M_2 = {m1} + {m2:.2f} = {m3:.2f} \text{{ kg}}")
                
        else:
            st.error("Error en los datos: La concentración final deseada debe ser menor que la concentración del azúcar añadido (100%).")
    
    # --- CAMBIO: Mensaje que se muestra antes de presionar el botón ---
    else:
        st.info("Por favor, ingresa tus datos y presiona 'Calcular Balance' para ver los resultados.")


# --- Pie de Página ---
st.markdown("---")
st.markdown("Creado con ❤️ por Natalia Valentina usando [Streamlit](https://streamlit.io).")


