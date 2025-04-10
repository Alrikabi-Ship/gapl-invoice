
from fpdf import FPDF
import streamlit as st

st.title("توليد الفاتورة")

dealer = st.text_input("اسم التاجر")
car_type = st.text_input("نوع السيارة")
amount_paid = st.text_input("المبلغ المدفوع")

if st.button("توليد الفاتورة"):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Amiri", "", "Amiri-Regular.ttf", uni=True)
    pdf.set_font("Amiri", size=14)

    pdf.cell(0, 10, txt=f"فاتورة GAPL: التاجر: {dealer}، نوع السيارة: {car_type}، المبلغ: {amount_paid}", ln=True)

    pdf.output("invoice.pdf")
    with open("invoice.pdf", "rb") as f:
        st.download_button("تحميل الفاتورة", f, file_name="invoice.pdf")
