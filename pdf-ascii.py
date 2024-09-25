from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont

mm = 2.83464567 # (1 mm = 2.83 pt)

# 名刺の幅と高さ (単位はポイント、1ポイント = 1/72インチ)
card_width = 55 * mm   # mm -> points 
card_height = 91 * mm  # mm -> points

# A4用紙の幅と高さ
page_width, page_height = landscape(A4)

# 名刺の列と行の数
columns = 5
rows = 2

# 余白の設定
margin_x = 11 * mm  # 左右の余白
margin_y = 14 * mm  # 上下の余白
padding  =  0 * mm  # 名刺間の余白

# 16進数の印刷順
HEX = [
	"09","0A","0D","1B","20", "22","25","30","33","2F", # p1表5x2
	"20","1B","0D","0A","09", "2F","33","30","25","22", # p1裏5x2(両面印刷)
	"2B","40","41","44","50", "5C","60","66","7A","7F", # p2表5x2
	"50","44","41","40","2B", "7F","7A","66","60","5C", # p2裏5x2(両面印刷)
]

# 10進数の印刷順（自動計算）
DEC = []
for i in range(len(HEX)):
	DEC.append(f"{int(HEX[i],16):2d}")

# スペース挿入関数
def insert_spaces(text):
	f = list(text)
	f.insert(4, " ")
	return "".join(f)

# 2進数の印刷順（自動計算）
BIN = []
for i in range(len(HEX)):
	BIN.append(insert_spaces(f"{int(HEX[i],16):08b}"))

# テキストの印刷順（自動計算）
TXT = {"00":"NUL", "09":"TAB", "0A":"LF", "0D":"CR", "1B":"ESC", "20":"SP", "7F":"DEL"}
for i in range(len(HEX)):
	if TXT.get(HEX[i]) == None:
		TXT[HEX[i]] = f"{int(HEX[i],16):c}"

# フォントの登録
registerFont(TTFont("Lucida Console", "/Windows/Fonts/lucon.ttf"))
registerFont(TTFont("Consolas", "/Windows/Fonts/consola.ttf"))

# PDFを生成する関数
def create_business_card_pdf(filename):
	c = canvas.Canvas(filename, pagesize=landscape(A4))
	
	# 各名刺の座標を計算して配置
	for i in range(len(HEX)):
		n = i % (rows * columns)
		p = i //(rows * columns)
		col = n % columns
		row = n //columns

		# 名刺の左下の位置を計算
		x = margin_x + col * (card_width + padding)
		y = page_height - (margin_y + (row + 1) * (card_height + padding))

		# 印刷機特性の微調整
		x = x + 3.0*mm

		# 名刺の枠を描画
		if p % 2 == 0:
			c.setStrokeColor(colors.royalblue) # Color(.254902,.411765,.882353,1)
			c.setLineWidth(24)
			c.rect(x, y, card_width, card_height)

		# 10進数表示
		if p % 2 == 1:
			c.setFont("Consolas", 28)
			c.drawString(x + 21*mm, y + card_height - 23*mm, DEC[i])

		# 16進数表示
		if p % 2 == 1:
			c.setFont("Consolas", 96)
			c.drawString(x + 9*mm, y + card_height - 58*mm, HEX[i])
		else:
			txt = TXT[HEX[i]]
			if len(txt) == 1:
				c.setFont("Consolas", 144)
				c.drawString(x + 14*mm, y + card_height - 61*mm, txt)
			elif len(txt) == 2:
				c.setFont("Consolas", 60)
				c.drawString(x + 17*mm, y + card_height - 53*mm, txt)
			else:
				c.setFont("Consolas", 60)
				c.drawString(x + 10*mm, y + card_height - 53*mm, txt)

		# 2進数表示
		if p % 2 == 1:
			c.setFont("Lucida Console", 18)
			c.drawString(x + 10*mm, y + card_height - 78*mm, BIN[i])

		# 下線を引く
		c.setStrokeColor(colors.black)
		c.setLineWidth(0.15)
		if p % 2 == 1:
			c.line(x + 10*mm, y + card_height - 63*mm, x + 45*mm, y + card_height - 63*mm)
		else:
			c.line(x + 10*mm, y + card_height - 75*mm, x + 45*mm, y + card_height - 75*mm)

		# 次ページに送る
		if (++i % (rows * columns) == rows * columns - 1):
			c.showPage()

	# PDFを保存
	if (i % (rows * columns) != rows * columns - 1):
		c.showPage()
	c.save()

# PDFファイルを生成
create_business_card_pdf("karuta-ascii.pdf")
