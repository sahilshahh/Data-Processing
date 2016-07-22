import os
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, cm


c = canvas.Canvas('C:/Users/ss5399/Desktop/report.pdf')
n = 0
# c.save()

# move the origin up and to the left, draw square
# c.translate(inch,9*inch)
# How do I make this rectangle link to google.com?
# c.rect(inch,inch,1*inch,1*inch, fill=1)
# c.linkURL('http://localhost:5000/download/Nokia_Logs/07_12_2016', (inch, inch, 2 * inch, 2 * inch),
          # relative=1)
for name in os.listdir('C:/Users/ss5399/Desktop/WebApp/static/graphs/Nokia_Logs/07_12_2016'):
    if n%2 == 0:
        c.drawImage('C:/Users/ss5399/Desktop/WebApp/static/graphs/Nokia_Logs/07_12_2016/'+name,35, 420, 19 * cm, 14 * cm)
        n=n+1
    else:
        c.drawImage('C:/Users/ss5399/Desktop/WebApp/static/graphs/Nokia_Logs/07_12_2016/' + name, 35, 20, 19 * cm,
                    14 * cm)
        n = n + 1
        c.showPage()
styleSheet = getSampleStyleSheet()
style = styleSheet['BodyText']
P=Paragraph('Download raw data <link href="http://localhost:5000/download/Nokia_Logs/07_12_2016" color ="blue">here</link>', style)
aW = 460 # available width and height
aH = 800
w,h = P.wrap(aW, aH) # find required space
if w<=aW and h<=aH:
    P.drawOn(c,250,250)
c.save()