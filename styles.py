"""
BeePower Stok Takip Sistemi - Stil Sistemi
Global stylesheet and color palette
"""

# Color palette
COLORS = {
    "bg_dark":       "#0f1117",
    "bg_panel":      "#1a1d2e",
    "bg_card":       "#1e2235",
    "bg_input":      "#252840",
    "accent":        "#f5a623",       # BeePower amber/honey
    "accent_hover":  "#ffb940",
    "accent_light":  "#ffd580",
    "green":         "#2ecc71",
    "green_dark":    "#27ae60",
    "red":           "#e74c3c",
    "red_dark":      "#c0392b",
    "orange":        "#e67e22",
    "orange_dark":   "#d35400",
    "blue":          "#3498db",
    "blue_dark":     "#2980b9",
    "text_primary":  "#ffffff",
    "text_secondary":"#a0a8c0",
    "text_muted":    "#606880",
    "border":        "#2e3250",
    "border_accent": "#f5a623",
    "row_even":      "#1a1d2e",
    "row_odd":       "#1e2235",
    "row_hover":     "#2a2f4a",
    "row_selected":  "#2d3561",
    "header_bg":     "#13162a",
    "tab_active":    "#f5a623",
    "tab_inactive":  "#1e2235",
    "status_available": "#2ecc71",
    "status_faulty":    "#e67e22",
    "status_unusable":  "#e74c3c",
}

STYLESHEET = f"""
/* ─── Global ─────────────────────────────────────────────────── */
QMainWindow, QDialog, QWidget {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
}}

/* ─── Left sidebar ────────────────────────────────────────────── */
#sidebar {{
    background-color: {COLORS['bg_panel']};
    border-right: 1px solid {COLORS['border']};
    min-width: 220px;
    max-width: 220px;
}}

#logo_label {{
    color: {COLORS['accent']};
    font-size: 18px;
    font-weight: 700;
    padding: 24px 16px 8px 16px;
    letter-spacing: 1px;
}}

#version_label {{
    color: {COLORS['text_muted']};
    font-size: 10px;
    padding: 0 16px 20px 16px;
}}

/* ─── Nav buttons ─────────────────────────────────────────────── */
QPushButton#nav_btn {{
    background-color: transparent;
    color: {COLORS['text_secondary']};
    border: none;
    border-left: 3px solid transparent;
    text-align: left;
    padding: 12px 16px;
    font-size: 13px;
    font-weight: 500;
    border-radius: 0px;
}}
QPushButton#nav_btn:hover {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
}}
QPushButton#nav_btn[active="true"] {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['accent']};
    border-left: 3px solid {COLORS['accent']};
    font-weight: 600;
}}

/* ─── Content area ────────────────────────────────────────────── */
#content_area {{
    background-color: {COLORS['bg_dark']};
}}

/* ─── Page title ──────────────────────────────────────────────── */
QLabel#page_title {{
    color: {COLORS['text_primary']};
    font-size: 22px;
    font-weight: 700;
    padding: 0px;
}}

QLabel#page_subtitle {{
    color: {COLORS['text_secondary']};
    font-size: 12px;
    padding-bottom: 4px;
}}

/* ─── Stat cards ──────────────────────────────────────────────── */
#stat_card {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    padding: 20px;
}}
#stat_value {{
    font-size: 36px;
    font-weight: 700;
    color: {COLORS['accent']};
}}
#stat_label {{
    font-size: 12px;
    color: {COLORS['text_secondary']};
    font-weight: 500;
}}

/* ─── Table ───────────────────────────────────────────────────── */
QTableWidget {{
    background-color: {COLORS['bg_panel']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    gridline-color: {COLORS['border']};
    selection-background-color: {COLORS['row_selected']};
    outline: none;
    alternate-background-color: {COLORS['row_odd']};
}}
QTableWidget::item {{
    padding: 8px 10px;
    border: none;
    color: {COLORS['text_primary']};
}}
QTableWidget::item:selected {{
    background-color: {COLORS['row_selected']};
    color: {COLORS['text_primary']};
}}
QTableWidget::item:hover {{
    background-color: {COLORS['row_hover']};
}}
QHeaderView::section {{
    background-color: {COLORS['header_bg']};
    color: {COLORS['text_secondary']};
    padding: 10px 10px;
    border: none;
    border-bottom: 2px solid {COLORS['border']};
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
QHeaderView::section:first {{
    border-top-left-radius: 8px;
}}
QHeaderView::section:last {{
    border-top-right-radius: 8px;
}}

/* ─── Buttons ─────────────────────────────────────────────────── */
QPushButton {{
    background-color: {COLORS['accent']};
    color: #000000;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 12px;
    min-height: 32px;
}}
QPushButton:hover {{
    background-color: {COLORS['accent_hover']};
}}
QPushButton:pressed {{
    background-color: {COLORS['accent_light']};
}}
QPushButton:disabled {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text_muted']};
}}

QPushButton#btn_secondary {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
}}
QPushButton#btn_secondary:hover {{
    background-color: {COLORS['bg_card']};
    border-color: {COLORS['accent']};
}}

QPushButton#btn_danger {{
    background-color: {COLORS['red']};
    color: #ffffff;
}}
QPushButton#btn_danger:hover {{
    background-color: {COLORS['red_dark']};
}}

QPushButton#btn_success {{
    background-color: {COLORS['green']};
    color: #ffffff;
}}
QPushButton#btn_success:hover {{
    background-color: {COLORS['green_dark']};
}}

QPushButton#btn_warning {{
    background-color: {COLORS['orange']};
    color: #ffffff;
}}
QPushButton#btn_warning:hover {{
    background-color: {COLORS['orange_dark']};
}}

/* ─── Line edits & combos ─────────────────────────────────────── */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 6px 10px;
    selection-background-color: {COLORS['accent']};
    selection-color: #000;
}}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {{
    border-color: {COLORS['accent']};
}}
QLineEdit::placeholder {{
    color: {COLORS['text_muted']};
}}

QComboBox {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 6px 10px;
    min-height: 30px;
}}
QComboBox:focus {{
    border-color: {COLORS['accent']};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox::down-arrow {{
    width: 10px;
    height: 10px;
}}
QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_panel']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    selection-background-color: {COLORS['row_selected']};
    outline: none;
}}

/* ─── Labels ──────────────────────────────────────────────────── */
QLabel {{
    color: {COLORS['text_primary']};
}}
QLabel#form_label {{
    color: {COLORS['text_secondary']};
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* ─── Tabs ────────────────────────────────────────────────────── */
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    background-color: {COLORS['bg_panel']};
}}
QTabBar::tab {{
    background-color: {COLORS['tab_inactive']};
    color: {COLORS['text_secondary']};
    padding: 10px 20px;
    border: none;
    border-radius: 0px;
    margin-right: 2px;
    font-weight: 500;
}}
QTabBar::tab:selected {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['accent']};
    border-bottom: 2px solid {COLORS['accent']};
    font-weight: 600;
}}
QTabBar::tab:hover:!selected {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
}}

/* ─── Scrollbars ──────────────────────────────────────────────── */
QScrollBar:vertical {{
    background: {COLORS['bg_panel']};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {COLORS['border']};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {COLORS['text_muted']};
}}
QScrollBar:horizontal {{
    background: {COLORS['bg_panel']};
    height: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: {COLORS['border']};
    border-radius: 4px;
    min-width: 30px;
}}
QScrollBar::add-line, QScrollBar::sub-line {{
    background: none;
}}

/* ─── Dialogs ─────────────────────────────────────────────────── */
QDialog {{
    background-color: {COLORS['bg_panel']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
}}
QDialog QLabel {{
    color: {COLORS['text_primary']};
}}
#dialog_title {{
    font-size: 16px;
    font-weight: 700;
    color: {COLORS['text_primary']};
    padding-bottom: 8px;
}}

/* ─── Search bar ──────────────────────────────────────────────── */
#search_bar {{
    background-color: {COLORS['bg_input']};
    border: 1px solid {COLORS['border']};
    border-radius: 20px;
    padding: 6px 14px;
    color: {COLORS['text_primary']};
    min-width: 250px;
}}
#search_bar:focus {{
    border-color: {COLORS['accent']};
}}

/* ─── Status badges ───────────────────────────────────────────── */
#badge_available {{
    background-color: {COLORS['status_available']};
    color: #fff;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}}
#badge_faulty {{
    background-color: {COLORS['status_faulty']};
    color: #fff;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}}
#badge_unusable {{
    background-color: {COLORS['status_unusable']};
    color: #fff;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}}

/* ─── Message boxes ───────────────────────────────────────────── */
QMessageBox {{
    background-color: {COLORS['bg_panel']};
    color: {COLORS['text_primary']};
}}
QMessageBox QPushButton {{
    min-width: 80px;
}}

/* ─── Spin box arrows ─────────────────────────────────────────── */
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    background-color: {COLORS['bg_card']};
    border: none;
    border-radius: 3px;
    width: 16px;
}}
QDateEdit::up-button, QDateEdit::down-button {{
    background-color: {COLORS['bg_card']};
    border: none;
    width: 16px;
}}
QDateEdit::drop-down {{
    background-color: {COLORS['bg_card']};
    border: none;
    width: 20px;
}}

/* ─── Separator ───────────────────────────────────────────────── */
QFrame[frameShape="4"], QFrame[frameShape="5"] {{
    color: {COLORS['border']};
}}

/* ─── Tool tips ───────────────────────────────────────────────── */
QToolTip {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 4px 8px;
}}
"""
