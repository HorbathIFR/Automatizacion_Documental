import streamlit as st
import pandas as pd
from datetime import datetime
from weasyprint import HTML

# =================== FUNCIONES COMUNES ===================

def cargar_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def llenar_html(template, datos):
    for clave, valor in datos.items():
        template = template.replace(f"{{{{{clave}}}}}", str(valor))
    return template

# =================== SIDEBAR ===================

st.sidebar.title("📋 Formularios")
seccion = st.sidebar.selectbox("Selecciona una sección:", [
    "📥 Recepción de equipos",
    "📤 Entrega de equipos"
])

# =================== RECEPCIÓN DE EQUIPOS ===================

if seccion == "📥 Recepción de equipos":
    st.title("📄 Acta de Recepción de Equipos")

    uploaded_file = st.file_uploader("🔼 Sube el archivo Excel de equipos", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        serial = st.text_input("🔍 Ingresa el número de serie del equipo")
        rol_empleado = st.text_input("🧾 Rol del empleado")

        if st.button("📥 Generar PDF"):
            serial_input = serial.strip().upper()
            df["Título"] = df["Título"].astype(str).str.strip().str.upper()
            equipo = df[df["Título"] == serial_input]

            if not equipo.empty:
                row = equipo.iloc[0]

                datos_equipo = {
                    "marca_modelo": f"{row['Fabricante']} {row['Modelo']}",
                    "serial": row["Número de serie"],
                    "procesador": row["Modelo de procesador"],
                    "ram": row["RAM"],
                    "disco": row["Capacidad"],
                    "inventario": row["Título"],
                    "entrega_nombre": row["Propietario actual"],
                    "rol_empleado": rol_empleado,
                    "fecha_actual": datetime.now().strftime("%d/%m/%Y")
                }

                html_template = cargar_html("recepcion.html")
                html_lleno = llenar_html(html_template, datos_equipo)
                pdf_bytes = HTML(string=html_lleno, base_url=".").write_pdf()

                st.success("✅ PDF generado exitosamente.")
                st.download_button(
                    label="⬇️ Descargar PDF",
                    data=pdf_bytes,
                    file_name=f"Acta_Recepcion_{serial_input}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("⚠️ No se encontró un equipo con ese número de serie.")

# =================== ENTREGA DE EQUIPOS ===================

elif seccion == "📤 Entrega de equipos":
    st.title("📦 Formulario de Entrega de Equipos")

    uploaded_file = st.file_uploader("🔼 Sube el archivo Excel de equipos", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        serial = st.text_input("🔍 Ingresa el número de serie del equipo")
        documento = st.text_input("📄 Número de documento")
        estado = st.selectbox("📌 Estado del equipo", ["Bueno", "Regular", "Malo"])
        empresa_nombre = st.selectbox("🏢 Empresa emisora", ["HORBATH TECHNOLOGIES", "GASES DEL CARIBE"])
        recibe_nombre = st.text_input("👤 Recibe (Nombre completo de quien recibe el equipo)")

        if st.button("📤 Generar PDF de Entrega"):
            serial_input = serial.strip().upper()
            df["Título"] = df["Título"].astype(str).str.strip().str.upper()
            equipo = df[df["Título"] == serial_input]

            if not equipo.empty:
                row = equipo.iloc[0]

                datos_equipo = {
                    "marca_modelo": f"{row['Fabricante']} {row['Modelo']}",
                    "serial": row["Número de serie"],
                    "procesador": row["Modelo de procesador"],
                    "ram": row["RAM"],
                    "disco": row["Capacidad"],
                    "inventario": row["Título"],
                    "entrega_nombre": recibe_nombre,
                    "fecha_actual": datetime.now().strftime("%d/%m/%Y"),
                    "numero_documento": documento,
                    "estado": estado,
                    "empresa_nombre": empresa_nombre
                }

                html_template = cargar_html("entrega.html")
                html_lleno = llenar_html(html_template, datos_equipo)
                pdf_bytes = HTML(string=html_lleno, base_url=".").write_pdf()

                st.success("✅ PDF generado exitosamente.")
                st.download_button(
                    label="⬇️ Descargar PDF",
                    data=pdf_bytes,
                    file_name=f"Entrega_{serial_input}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("⚠️ No se encontró un equipo con ese número de serie.")