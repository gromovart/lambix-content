from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

OUTPUT = "/tmp/brief_lambix_trade.pdf"

# Цвета лендинга
BG       = colors.HexColor("#0D0D0D")
ORANGE   = colors.HexColor("#F59E0B")
WHITE    = colors.HexColor("#FFFFFF")
GRAY     = colors.HexColor("#9CA3AF")
DARK2    = colors.HexColor("#1A1A1A")
BORDER   = colors.HexColor("#2A2A2A")

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
)

W, H = A4

def S(font="Arial", size=10, color=WHITE, align=TA_LEFT, after=4, before=0, leading=15, bold=False):
    return ParagraphStyle("_",
        fontName="Arial-Bold" if bold else font,
        fontSize=size, textColor=color,
        alignment=align, spaceAfter=after,
        spaceBefore=before, leading=leading,
        backColor=None,
    )

H1     = S(size=28, color=WHITE, bold=True, leading=32, after=2)
ORANGE_LINE_STYLE = S(size=11, color=ORANGE, leading=14, after=10)
H2     = S(size=13, color=ORANGE, bold=True, before=16, after=6, leading=18)
BODY   = S(size=10, color=WHITE, after=4)
MUTED  = S(size=10, color=GRAY, after=4)
CENTER = S(size=10, color=GRAY, align=TA_CENTER)

KEY_STYLE  = S(size=10, color=ORANGE, bold=True, after=0, leading=14)
VAL_STYLE  = S(size=10, color=GRAY,   after=0, leading=14)
VAL_WHITE  = S(size=10, color=WHITE,  after=0, leading=14)

def dark_table(data, col_widths=None):
    if col_widths is None:
        col_widths = [4*cm, 12*cm]
    rows = [[Paragraph(str(k), KEY_STYLE), Paragraph(str(v), VAL_WHITE)] for k, v in data]
    t = Table(rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), DARK2),
        ("BACKGROUND",  (0, 0), (0, -1), colors.HexColor("#1F1F1F")),
        ("PADDING",     (0, 0), (-1, -1), 8),
        ("GRID",        (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
    ]))
    return t

def feat_table(data):
    rows = [[Paragraph(str(k), KEY_STYLE), Paragraph(str(v), VAL_STYLE)] for k, v in data]
    t = Table(rows, colWidths=[5*cm, 11*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), DARK2),
        ("BACKGROUND",  (0, 0), (0, -1), colors.HexColor("#1A1A1A")),
        ("PADDING",     (0, 0), (-1, -1), 8),
        ("GRID",        (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
    ]))
    return t

# Фоновый прямоугольник на всю страницу — через первый элемент таблицы
def bg_header():
    t = Table([["  "]], colWidths=[W - 4*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BG),
        ("PADDING", (0,0), (-1,-1), 0),
        ("BOX", (0,0), (-1,-1), 0, BG),
    ]))
    return t

story = []

# --- Логотип / шапка ---
story.append(Paragraph("LambixTrade", H1))
story.append(HRFlowable(width="100%", thickness=3, color=ORANGE, spaceAfter=6))
story.append(Paragraph("Бриф для инфлюенсера · Бета-тестирование платформы", ORANGE_LINE_STYLE))

# --- О продукте ---
story.append(Paragraph("О продукте", H2))
story.append(dark_table([
    ["Продукт",  "LambixTrade — торговая платформа для Bybit и BingX"],
    ["Лендинг",  "https://trade.lambix.ru/"],
    ["Платформа","https://app.lambix.ru/"],
    ["Группа",   "https://t.me/+NBoWij3wowNlNTEy"],
    ["Формат",   "Бета-тестирование — 100 мест"],
    ["Доступ",   "Через Telegram-группу (вручную по TG ID)"],
]))

# --- О платформе ---
story.append(Paragraph("О платформе", H2))
story.append(Paragraph(
    "Рабочее место трейдера с дашбордом риска, журналом сделок, целями по прибыли и сигналами. "
    "Подключи Bybit и BingX — остальное уже внутри. "
    "Инструменты как в проп-компании — для своего счёта, без % от прибыли и чужих правил.",
    BODY
))

# --- Ключевой функционал ---
story.append(Paragraph("Ключевой функционал", H2))
story.append(feat_table([
    ["Bybit + BingX в одном окне",    "Спот и фьючерс обеих бирж. Общий PnL портфеля виден сразу."],
    ["Управление позицией",            "Усреднение, частичное закрытие, перенос стопа, безубыток, трейлинг — по одной кнопке."],
    ["Риск-менеджмент",                "Цена ликвидации, свободная маржа, риск на сделку от баланса — автоматически."],
    ["Цели и дисциплина",              "Установи дневной план по прибыли и следи за прогрессом — как в проп-компании."],
    ["Журнал с разбором",              "Реальный Win Rate, история по символам, анализ где теряешь."],
    ["Конструктор сетапов",            "Проверяй торговые идеи без реальных средств: R:R, TP/SL в эмуляторе."],
    ["Сигналы",                        "Скоринг 500+ монет по 17 факторам (RSI, OI, тренд, фандинг). Режимы: Скальп, Интрадей, Свинг."],
]))

# --- Ценность ---
story.append(Paragraph("Ценность для аудитории", H2))
story.append(Paragraph(
    "Проп-фирмы дают трейдерам дашборд риска, контроль просадки и журнал — потому что без системы деньги сливаются. "
    "LambixTrade даёт то же самое для личного счёта на Bybit и BingX: видишь риск до входа, контролируешь цель по дню, знаешь где теряешь.",
    BODY
))

# --- Что получает аудитория ---
story.append(Paragraph("Что получает аудитория", H2))
for b in [
    "Бесплатный доступ на 10 дней (3 дня стандартный триал + 7 дней бонус за участие в тесте)",
    "Возможность протестировать продукт первыми, до публичного запуска",
    "Прямая связь с командой — фидбек учитывается в продукте",
]:
    story.append(Paragraph(f"•  {b}", BODY))

# --- Задача ---
story.append(Paragraph("Задача", H2))
story.append(Paragraph(
    "Нативный пост в канале с призывом вступить в Telegram-группу. "
    "Цель — привлечь активных трейдеров, которым интересен новый инструмент для Bybit/BingX.",
    BODY
))

# --- Ключевые тезисы ---
story.append(Paragraph("Ключевые тезисы (обязательные)", H2))
for i, p in enumerate([
    "Новая торговая платформа — Bybit + BingX в одном интерфейсе",
    "Только 100 мест — бета-тест, первые 100 участников",
    "Бесплатно для участников теста",
], 1):
    story.append(Paragraph(f"{i}.  {p}", BODY))

# --- Формат поста ---
story.append(Paragraph("Формат поста", H2))
story.append(dark_table([
    ["Объём",   "800–1500 символов"],
    ["Стиль",   "Нативный, от первого лица, без технических деталей"],
    ["CTA",     "Одна ссылка/кнопка → Telegram-бот → Telegram-группа"],
    ["Время",   "12:00–14:00 или 19:00–21:00 МСК"],
]))

# --- Ограничения ---
story.append(Paragraph("Ограничения", H2))
for r in [
    'Не упоминать "заработок", "сигналы", "гарантированную прибыль"',
    "Не использовать стоковые визуалы — только скриншоты платформы (предоставим)",
]:
    story.append(Paragraph(f"—  {r}", MUTED))

# --- Материалы ---
story.append(Paragraph("Материалы от нас", H2))
for m in [
    "Ссылка на Telegram-группу",
    "Скриншоты интерфейса платформы",
    "Краткое описание функционала",
]:
    story.append(Paragraph(f"[ ]  {m}", BODY))

# --- Контакт ---
story.append(Spacer(1, 14))
story.append(HRFlowable(width="100%", thickness=1, color=BORDER))
story.append(Spacer(1, 8))
story.append(Paragraph("Контакт: Артём Громов — @artemgrrr", CENTER))

# Тёмный фон для всей страницы через canvasmaker
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.pagesizes import A4

class DarkDoc(SimpleDocTemplate):
    def handle_pageBegin(self):
        self.canv.setFillColor(BG)
        self.canv.rect(0, 0, self.pagesize[0], self.pagesize[1], fill=1, stroke=0)
        super().handle_pageBegin()

doc2 = DarkDoc(
    OUTPUT,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
)
doc2.build(story)
print("OK:", OUTPUT)
