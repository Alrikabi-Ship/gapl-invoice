
import streamlit as st
from fpdf import FPDF
from PIL import Image
from datetime import date

st.set_page_config(page_title="GAPL Invoice Generator", layout="centered")

st.title("GAPL Invoice Generator")

with st.form("invoice_form"):
    dealer = st.text_input("Dealer Name")
    car_type = st.text_input("Car Type")
    amount_paid = st.text_input("Amount Paid (USD)")
    invoice_date = st.date_input("Invoice Date", value=date.today())
    submitted = st.form_submit_button("Generate Invoice")

if submitted:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.image("logo.png", x=10, y=8, w=33)
    pdf.ln(30)
    pdf.cell(200, 10, txt="GAPL - Global Auto Parts Logistics", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Invoice Date: {invoice_date}", ln=True)
    pdf.cell(200, 10, txt=f"Dealer: {dealer}", ln=True)
    pdf.cell(200, 10, txt=f"Car Type: {car_type}", ln=True)
    pdf.cell(200, 10, txt=f"Amount Paid: ${amount_paid}", ln=True)
    pdf.ln(10)
    pdf.set_text_color(0, 0, 255)
    msg = f"GAPL Invoice:\nDealer: {dealer}\nCar: {car_type}\nAmount: ${amount_paid}"
    wa_link = f"https://wa.me/?text={msg.replace(' ', '%20')}"
    pdf.cell(200, 10, txt="Share via WhatsApp", ln=True, link=wa_link)
    pdf.set_text_color(0, 0, 0)
    pdf.output("invoice.pdf")
    with open("invoice.pdf", "rb") as f:
        st.download_button("Download Invoice PDF", f, file_name="invoice.pdf")
    st.markdown(f"[Open WhatsApp Link]({wa_link})")
