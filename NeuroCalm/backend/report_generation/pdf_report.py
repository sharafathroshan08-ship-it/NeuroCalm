import os
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether
)


# ============================================================
# NEUROCALM - PROFESSIONAL PDF REPORT
# ============================================================

def create_pdf(
    file_path,
    current_score,
    current_level,
    average_score,
    trend,
    history,
    top_factors,
    recommendations,
    user_name
):

    # --------------------------------------------------------
    # Create output folder if it does not exist
    # --------------------------------------------------------

    output_folder = os.path.dirname(file_path)

    if output_folder:
        os.makedirs(output_folder, exist_ok=True)


    # --------------------------------------------------------
    # Page setup
    # --------------------------------------------------------

    PAGE_WIDTH, PAGE_HEIGHT = A4

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=24 * mm,
        bottomMargin=18 * mm
    )


    # --------------------------------------------------------
    # Colors
    # --------------------------------------------------------

    NAVY = colors.HexColor("#17365D")
    BLUE = colors.HexColor("#2F75B5")
    LIGHT_BLUE = colors.HexColor("#EAF3F8")

    DARK_TEXT = colors.HexColor("#202124")
    GREY_TEXT = colors.HexColor("#5F6368")
    LIGHT_GREY = colors.HexColor("#F4F6F8")
    BORDER = colors.HexColor("#D9E0E6")

    GREEN = colors.HexColor("#2E7D32")
    LIGHT_GREEN = colors.HexColor("#EAF5EA")

    ORANGE = colors.HexColor("#C77C00")
    LIGHT_ORANGE = colors.HexColor("#FFF4DD")

    RED = colors.HexColor("#B3261E")
    LIGHT_RED = colors.HexColor("#FDECEC")

    WHITE = colors.white


    # --------------------------------------------------------
    # Determine stress color
    # --------------------------------------------------------

    level_text = str(current_level).strip().lower()

    if level_text == "low":
        level_color = GREEN
        level_background = LIGHT_GREEN

    elif level_text == "high":
        level_color = RED
        level_background = LIGHT_RED

    else:
        level_color = ORANGE
        level_background = LIGHT_ORANGE


    # --------------------------------------------------------
    # Clean text
    # --------------------------------------------------------

    def safe_text(value):
        if value is None:
            return ""

        return escape(str(value))


    def clean_trend(value):
        text = str(value)

        replacements = {
            "↗️": "",
            "↗": "",
            "↘️": "",
            "↘": "",
            "→": "",
            "⬆️": "",
            "⬇️": "",
            "⬆": "",
            "⬇": "",
            "■": ""
        }

        for symbol, replacement in replacements.items():
            text = text.replace(symbol, replacement)

        return text.strip()


    trend_text = clean_trend(trend)


    # --------------------------------------------------------
    # Styles
    # --------------------------------------------------------

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=27,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=GREY_TEXT,
        alignment=TA_LEFT
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=NAVY,
        spaceBefore=5,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "NormalText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=DARK_TEXT
    )

    small_style = ParagraphStyle(
        "SmallText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=GREY_TEXT
    )

    card_label_style = ParagraphStyle(
        "CardLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=10,
        textColor=GREY_TEXT,
        alignment=TA_CENTER
    )

    card_value_style = ParagraphStyle(
        "CardValue",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=19,
        textColor=NAVY,
        alignment=TA_CENTER
    )

    score_style = ParagraphStyle(
        "Score",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=31,
        leading=34,
        textColor=level_color,
        alignment=TA_CENTER
    )

    score_label_style = ParagraphStyle(
        "ScoreLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=GREY_TEXT,
        alignment=TA_CENTER
    )

    factor_name_style = ParagraphStyle(
        "FactorName",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=DARK_TEXT
    )

    factor_effect_style = ParagraphStyle(
        "FactorEffect",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=GREY_TEXT
    )

    recommendation_style = ParagraphStyle(
        "Recommendation",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT
    )

    white_center_style = ParagraphStyle(
        "WhiteCenter",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=WHITE,
        alignment=TA_CENTER
    )


    # --------------------------------------------------------
    # Header and Footer
    # --------------------------------------------------------

    def draw_header_footer(canvas, document):

        canvas.saveState()

        # Top header line
        canvas.setFillColor(NAVY)
        canvas.rect(
            0,
            PAGE_HEIGHT - 7 * mm,
            PAGE_WIDTH,
            7 * mm,
            fill=1,
            stroke=0
        )

        # Footer line
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.6)

        canvas.line(
            16 * mm,
            12 * mm,
            PAGE_WIDTH - 16 * mm,
            12 * mm
        )

        # Footer text
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(GREY_TEXT)

        canvas.drawString(
            16 * mm,
            7 * mm,
            "NeuroCalm | Stress Monitoring and Wellbeing Support System"
        )

        canvas.drawRightString(
            PAGE_WIDTH - 16 * mm,
            7 * mm,
            f"Page {document.page}"
        )

        canvas.restoreState()


    # --------------------------------------------------------
    # Main story
    # --------------------------------------------------------

    story = []


    # ========================================================
    # PAGE 1
    # ========================================================

    # Title block

    title_block = Table(
        [
            [
                Paragraph(
                    "NeuroCalm",
                    title_style
                )
            ],
            [
                Paragraph(
                    "Stress Assessment Report",
                    ParagraphStyle(
                        "ReportSubTitle",
                        parent=subtitle_style,
                        fontSize=12,
                        textColor=BLUE
                    )
                )
            ],
            [
                Paragraph(
                    "Personalized stress analysis based on the latest assessment",
                    subtitle_style
                )
            ]
        ],
        colWidths=[178 * mm]
    )

    title_block.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )

    story.append(title_block)

    story.append(Spacer(1, 5 * mm))


    # --------------------------------------------------------
    # User information
    # --------------------------------------------------------

    user_name = str(user_name).strip()

    if not user_name:
        user_name = "User"

    user_info = Table(
        [
            [
                Paragraph(
                    "<b>USER NAME</b>",
                    small_style
                ),
                Paragraph(
                    safe_text(user_name),
                    ParagraphStyle(
                        "UserName",
                        parent=normal_style,
                        fontName="Helvetica-Bold",
                        fontSize=10,
                        textColor=NAVY
                    )
                )
            ]
        ],
        colWidths=[
            40 * mm,
            138 * mm
        ]
    )

    user_info.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), LIGHT_BLUE),
                ("BACKGROUND", (1, 0), (1, 0), WHITE),

                ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),

                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    story.append(user_info)

    story.append(Spacer(1, 5 * mm))

    # Report metadata

    generated_time = datetime.now().strftime(
        "%d %b %Y, %H:%M"
    )

    metadata = Table(
        [
            [
                Paragraph(
                    "<b>REPORT TYPE</b><br/>Student Stress Assessment",
                    small_style
                ),
                Paragraph(
                    "<b>GENERATED</b><br/>" + safe_text(generated_time),
                    small_style
                ),
                Paragraph(
                    "<b>ASSESSMENT STATUS</b><br/>Completed",
                    small_style
                )
            ]
        ],
        colWidths=[
            59 * mm,
            59 * mm,
            59 * mm
        ]
    )

    metadata.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(metadata)

    story.append(Spacer(1, 7 * mm))


    # --------------------------------------------------------
    # Current result
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "1. CURRENT STRESS RESULT",
            section_style
        )
    )


    # Big score card

    score_card = Table(
        [
            [
                Paragraph(
                    f"{float(current_score):.0f}%",
                    score_style
                ),
                Paragraph(
                    safe_text(current_level),
                    ParagraphStyle(
                        "LevelLarge",
                        parent=card_value_style,
                        fontSize=18,
                        textColor=level_color
                    )
                ),
                Paragraph(
                    f"{float(average_score):.0f}%",
                    card_value_style
                ),
                Paragraph(
                    safe_text(trend_text),
                    ParagraphStyle(
                        "TrendValue",
                        parent=card_value_style,
                        fontSize=13,
                        textColor=BLUE
                    )
                )
            ],
            [
                Paragraph(
                    "CURRENT STRESS SCORE",
                    score_label_style
                ),
                Paragraph(
                    "STRESS LEVEL",
                    card_label_style
                ),
                Paragraph(
                    "AVERAGE SCORE",
                    card_label_style
                ),
                Paragraph(
                    "CURRENT TREND",
                    card_label_style
                )
            ]
        ],
        colWidths=[
            44 * mm,
            44 * mm,
            44 * mm,
            44 * mm
        ]
    )

    score_card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), level_background),
                ("BACKGROUND", (1, 0), (1, -1), level_background),
                ("BACKGROUND", (2, 0), (2, -1), LIGHT_BLUE),
                ("BACKGROUND", (3, 0), (3, -1), LIGHT_BLUE),

                ("BOX", (0, 0), (-1, -1), 0.8, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                ("TOPPADDING", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 3),

                ("TOPPADDING", (0, 1), (-1, 1), 4),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
            ]
        )
    )

    story.append(score_card)

    story.append(Spacer(1, 7 * mm))


    # --------------------------------------------------------
    # Main factors
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "2. MAIN STRESS FACTORS",
            section_style
        )
    )

    factor_rows = [
        [
            Paragraph("<b>#</b>", white_center_style),
            Paragraph("<b>FACTOR</b>", white_center_style),
            Paragraph("<b>OBSERVED EFFECT</b>", white_center_style)
        ]
    ]


    for index, factor in enumerate(top_factors, start=1):

        if isinstance(factor, dict):

            factor_name = factor.get("name", "")
            effect = factor.get("effect", "")

        else:

            try:
                factor_name = factor[0]
                effect = factor[1]
            except Exception:
                factor_name = str(factor)
                effect = ""


        factor_rows.append(
            [
                Paragraph(
                    str(index),
                    ParagraphStyle(
                        "FactorNumber",
                        parent=normal_style,
                        fontName="Helvetica-Bold",
                        fontSize=9,
                        textColor=BLUE,
                        alignment=TA_CENTER
                    )
                ),

                Paragraph(
                    safe_text(factor_name),
                    factor_name_style
                ),

                Paragraph(
                    safe_text(effect),
                    factor_effect_style
                )
            ]
        )


    if len(factor_rows) == 1:

        factor_rows.append(
            [
                Paragraph("-", normal_style),
                Paragraph("No factor information available.", normal_style),
                Paragraph("", normal_style)
            ]
        )


    factor_table = Table(
        factor_rows,
        colWidths=[
            12 * mm,
            67 * mm,
            99 * mm
        ],
        repeatRows=1
    )

    factor_style_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]


    for row_index in range(1, len(factor_rows)):

        effect_text = ""

        if isinstance(top_factors[row_index - 1], dict):
            effect_text = str(
                top_factors[row_index - 1].get("effect", "")
            ).lower()

        else:
            try:
                effect_text = str(
                    top_factors[row_index - 1][1]
                ).lower()
            except Exception:
                pass


        if "higher" in effect_text:

            factor_style_commands.append(
                (
                    "BACKGROUND",
                    (2, row_index),
                    (2, row_index),
                    LIGHT_RED
                )
            )

        else:

            factor_style_commands.append(
                (
                    "BACKGROUND",
                    (2, row_index),
                    (2, row_index),
                    LIGHT_GREEN
                )
            )


        if row_index % 2 == 0:

            factor_style_commands.append(
                (
                    "BACKGROUND",
                    (0, row_index),
                    (1, row_index),
                    LIGHT_GREY
                )
            )


    factor_table.setStyle(
        TableStyle(factor_style_commands)
    )

    story.append(factor_table)

    story.append(Spacer(1, 6 * mm))


    # --------------------------------------------------------
    # Why this result?
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "3. WHY THIS RESULT?",
            section_style
        )
    )

    higher_count = 0
    lower_count = 0

    for factor in top_factors:

        if isinstance(factor, dict):

            effect = str(
                factor.get("effect", "")
            ).lower()

        else:

            try:
                effect = str(factor[1]).lower()
            except Exception:
                effect = ""


        if "higher" in effect:
            higher_count += 1
        elif "lower" in effect:
            lower_count += 1


    if higher_count > lower_count:

        why_text = (
            "The current result is mainly influenced by factors "
            "associated with increased stress."
            "<br/>"
            "Addressing the key contributing factors may help improve "
            "overall stress levels."
        )

    elif lower_count > higher_count:

        why_text = (
            "Several factors are currently associated with lower stress."
            "<br/>"
            "Maintaining these positive factors may support continued wellbeing."
        )

    else:

        why_text = (
            "The result reflects a combination of higher- and lower-stress "
            "contributing factors."
            "<br/>"
            "Small improvements in the main contributing areas may help."
        )


    why_box = Table(
        [
            [
                Paragraph(
                    why_text,
                    normal_style
                )
            ]
        ],
        colWidths=[178 * mm]
    )

    why_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.8, BLUE),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )

    story.append(why_box)

    story.append(Spacer(1, 6 * mm))


    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "4. PERSONALIZED RECOMMENDATIONS",
            section_style
        )
    )

    recommendation_rows = []

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        recommendation_rows.append(
            [
                Paragraph(
                    f"{index}",
                    ParagraphStyle(
                        "RecNumber",
                        parent=normal_style,
                        fontName="Helvetica-Bold",
                        fontSize=10,
                        textColor=BLUE,
                        alignment=TA_CENTER
                    )
                ),

                Paragraph(
                    safe_text(recommendation),
                    recommendation_style
                )
            ]
        )


    if not recommendation_rows:

        recommendation_rows.append(
            [
                Paragraph("-", normal_style),
                Paragraph(
                    "No personalized recommendations available.",
                    recommendation_style
                )
            ]
        )


    recommendation_table = Table(
        recommendation_rows,
        colWidths=[
            13 * mm,
            165 * mm
        ]
    )

    recommendation_commands = [
        ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),

        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]


    for row_index in range(len(recommendation_rows)):

        if row_index % 2 == 1:

            recommendation_commands.append(
                (
                    "BACKGROUND",
                    (1, row_index),
                    (1, row_index),
                    LIGHT_GREY
                )
            )


    recommendation_table.setStyle(
        TableStyle(recommendation_commands)
    )

    story.append(recommendation_table)


    # ========================================================
    # PAGE 2
    # ========================================================

    story.append(PageBreak())


    # --------------------------------------------------------
    # Page 2 title
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "NeuroCalm - Assessment Analytics",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Stress scale and historical assessment overview",
            subtitle_style
        )
    )

    story.append(Spacer(1, 7 * mm))


    # --------------------------------------------------------
    # Stress scale
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "5. STRESS LEVEL SCALE",
            section_style
        )
    )


    scale_rows = [
        [
            Paragraph("LOW", white_center_style),
            Paragraph("MODERATE", white_center_style),
            Paragraph("HIGH", white_center_style)
        ],
        [
            Paragraph("0 - 33%", white_center_style),
            Paragraph("34 - 66%", white_center_style),
            Paragraph("67 - 100%", white_center_style)
        ]
    ]


    scale_table = Table(
        scale_rows,
        colWidths=[
            59 * mm,
            59 * mm,
            59 * mm
        ]
    )


    scale_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), GREEN),
                ("BACKGROUND", (1, 0), (1, -1), ORANGE),
                ("BACKGROUND", (2, 0), (2, -1), RED),

                ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, WHITE),

                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )


    story.append(scale_table)

    story.append(Spacer(1, 4 * mm))


    current_marker = Table(
        [
            [
                Paragraph(
                    f"Current assessment: {float(current_score):.0f}% "
                    f"- {safe_text(current_level)}",
                    ParagraphStyle(
                        "Marker",
                        parent=normal_style,
                        fontName="Helvetica-Bold",
                        fontSize=9,
                        textColor=level_color,
                        alignment=TA_CENTER
                    )
                )
            ]
        ],
        colWidths=[178 * mm]
    )

    current_marker.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), level_background),
                ("BOX", (0, 0), (-1, -1), 0.7, level_color),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(current_marker)

    story.append(Spacer(1, 8 * mm))


    # --------------------------------------------------------
    # Historical data
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "6. STRESS HISTORY",
            section_style
        )
    )


    history_rows = [
        [
            Paragraph("<b>DATE</b>", white_center_style),
            Paragraph("<b>TIME</b>", white_center_style),
            Paragraph("<b>SCORE</b>", white_center_style),
            Paragraph("<b>LEVEL</b>", white_center_style)
        ]
    ]


    try:

        history_records = history.to_dict(
            orient="records"
        )

    except Exception:

        history_records = []


    for item in history_records:

        date_value = safe_text(
            item.get("date", "")
        )

        time_value = safe_text(
            item.get("time", "")
        )

        score_value = item.get(
            "stress_score",
            ""
        )

        level_value = safe_text(
            item.get("stress_level", "")
        )


        try:
            score_display = f"{float(score_value):.0f}%"
        except Exception:
            score_display = safe_text(score_value)


        history_rows.append(
            [
                Paragraph(date_value, normal_style),
                Paragraph(time_value, normal_style),
                Paragraph(
                    score_display,
                    ParagraphStyle(
                        "HistoryScore",
                        parent=normal_style,
                        fontName="Helvetica-Bold",
                        textColor=NAVY
                    )
                ),
                Paragraph(level_value, normal_style)
            ]
        )


    if len(history_rows) == 1:

        history_rows.append(
            [
                Paragraph("-", normal_style),
                Paragraph("-", normal_style),
                Paragraph("-", normal_style),
                Paragraph("No history available", normal_style)
            ]
        )


    history_table = Table(
        history_rows,
        colWidths=[
            43 * mm,
            43 * mm,
            43 * mm,
            49 * mm
        ],
        repeatRows=1
    )


    history_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),

        ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]


    for row_index in range(1, len(history_rows)):

        if row_index % 2 == 0:

            history_commands.append(
                (
                    "BACKGROUND",
                    (0, row_index),
                    (-1, row_index),
                    LIGHT_GREY
                )
            )


    history_table.setStyle(
        TableStyle(history_commands)
    )

    story.append(history_table)

    story.append(Spacer(1, 8 * mm))


    # --------------------------------------------------------
    # Summary box
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "7. ASSESSMENT SUMMARY",
            section_style
        )
    )


    summary_text = (
        f"The latest assessment recorded a stress score of "
        f"<b>{float(current_score):.0f}%</b>, classified as "
        f"<b>{safe_text(current_level)}</b>. "
        f"The overall average across available assessments is "
        f"<b>{float(average_score):.0f}%</b>."
        f"<br/><br/>"
        f"Current trend: <b>{safe_text(trend_text)}</b>."
    )


    summary_box = Table(
        [
            [
                Paragraph(
                    summary_text,
                    normal_style
                )
            ]
        ],
        colWidths=[178 * mm]
    )


    summary_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
                ("BOX", (0, 0), (-1, -1), 0.8, BORDER),

                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )


    story.append(summary_box)

    story.append(Spacer(1, 7 * mm))


    # --------------------------------------------------------
    # Final note
    # --------------------------------------------------------

    final_note = Table(
        [
            [
                Paragraph(
                    "<b>NeuroCalm</b> provides stress monitoring, "
                    "factor-based analysis and personalized wellbeing "
                    "support using the assessment data.",
                    small_style
                )
            ]
        ],
        colWidths=[178 * mm]
    )


    final_note.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),

                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )


    story.append(final_note)


    # --------------------------------------------------------
    # Build PDF
    # --------------------------------------------------------

    doc.build(
        story,
        onFirstPage=draw_header_footer,
        onLaterPages=draw_header_footer
    )


# ============================================================
# END OF FILE
# ============================================================