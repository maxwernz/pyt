from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

c = canvas.Canvas("hello.pdf", pagesize=A4, bottomup=0)
def hello(c):
    c.drawString(100, 100, "Hello")
width, height = A4
c.line(0, height-100, width, height-100)
c.drawInlineImage("eu.pgm", 0, -100, 100, 100)

c.showPage()
c.save()