
import streamlit as st
import qrcode
from io import BytesIO
from fpdf import FPDF
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="نموذج توليد فاتورة GAPL", layout="centered")
st.title("نموذج توليد فاتورة PDF - GAPL")
st.markdown("املأ البيانات التالية لتوليد فاتورة رسمية بصيغة PDF")

# from pathlib import Pathنموذج الإدخال
supplier = st.text_input("اسم المورد")
dealer = st.text_input("اسم التاجر")
car_type = st.text_input("نوع السيارة")
car_model = st.text_input("موديل السيارة")
purchase_date = st.date_input("تاريخ شراء السيارة")
payment_date = st.date_input("تاريخ الدفع")
amount_paid = st.text_input("المبلغ المدفوع")
total_amount = st.text_input("إجمالي الصفقة")
balance = st.text_input("الرصيد المتبقي")
status = st.selectbox("حالة الصفقة", ["قيد التنفيذ", "تم التسليم", "ملغاة"])
notes = st.text_area("ملاحظات")
logo_path = "gapl_logo.png"

if st.button("توليد الفاتورة"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    if Path(logo_path).exists():
        pdf.image(logo_path, x=10, y=8, w=33)
        pdf.ln(30)
    pdf.cell(0, 10, "فاتورة مفصلة", ln=True, align='C')
    pdf.ln(10)

    def row(label, value):
        pdf.cell(60, 10, label, border=1)
        pdf.cell(0, 10, value, border=1, ln=True)

    row("اسم المورد", supplier)
    row("اسم التاجر", dealer)
    row("نوع السيارة", car_type)
    row("موديل السيارة", car_model)
    row("تاريخ الشراء", str(purchase_date))
    row("تاريخ الدفع", str(payment_date))
    row("المبلغ المدفوع", amount_paid)
    row("إجمالي الصفقة", total_amount)
    row("الرصيد المتبقي", balance)
    row("حالة الصفقة", status)
    row("ملاحظات", notes)

    msg = f"فاتورة GAPL:\nالتاجر: {dealer}\nنوع السيارة: {car_type}\nالمبلغ: {amount_paid}"
    wa_link = f"https://wa.me/?text={msg.replace(' ', '%20')}"
    st.markdown(f"[مشاركة على واتساب]({wa_link})")

    qr = qrcode.make(wa_link)
    qr_bytes = BytesIO()
    qr.save(qr_bytes, format="PNG")
    qr_bytes.seek(0)
    pdf.image(qr_bytes, x=80, w=50)

    pdf.ln(10)
    pdf.cell(0, 10, "قسم: مدير قسم الاستيراد", ln=True)

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    st.download_button("تحميل الفاتورة PDF", data=pdf_output.getvalue(), file_name="invoice.pdf")
