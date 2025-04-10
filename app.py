
import streamlit as st
import qrcode
from io import BytesIO
from fpdf import FPDF
from PIL import Image

st.set_page_config(page_title="فاتورة GAPL", page_icon=":receipt:", layout="centered")
st.title("نموذج توليد فاتورة PDF - GAPL")
st.markdown("املأ البيانات التالية لتوليد فاتورة رسمية بصيغة PDF")

# نموذج الإدخال
supplier = st.text_input("اسم المورد")
dealer = st.text_input("اسم التاجر")
car_type = st.text_input("نوع السيارة")
car_model = st.text_input("موديل السيارة")
purchase_date = st.date_input("تاريخ شراء السيارة")
payment_date = st.date_input("تاريخ الدفع")
amount_paid = st.text_input("المبلغ المدفوع")
total_amount = st.text_input("إجمالي الصفقة")
balance = st.text_input("الرصيد المتبقي")
status = st.selectbox("حالة الصفقة", ["قيد التنفيذ", "مكتملة", "ملغية"])
notes = st.text_area("ملاحظات")

if st.button("توليد الفاتورة"):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Arial", "", fname="arial.ttf", uni=True)
    pdf.set_font("Arial", size=14)

    # إضافة الشعار
    pdf.image("gapl_logo.png", x=80, w=50)
    pdf.ln(10)

    pdf.cell(0, 10, "فاتورة صفقة", ln=True, align="C")
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

    # QR Code
    msg = f"فاتورة GAPL من التاجر: {dealer}\nنوع السيارة: {car_type}\nالمبلغ: {amount_paid}"
    qr = qrcode.make(msg)
    qr_bytes = BytesIO()
    qr.save(qr_bytes)
    qr_bytes.seek(0)
    pdf.image(qr_bytes, x=80, w=50)
    pdf.ln(10)

    pdf.cell(0, 10, "قسم: مدير قسم الاستيراد", ln=True)

    output = BytesIO()
    pdf.output(output)
    st.download_button("تحميل الفاتورة PDF", data=output.getvalue(), file_name="invoice.pdf")

    # رابط واتساب
    wa_link = f"https://wa.me/?text={msg.replace(' ', '%20')}"
    st.markdown(f"[مشاركة على واتساب]({wa_link})")
