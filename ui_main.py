"""
BeePower Stok Takip Sistemi - Ana Pencere
Main application window
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame,
    QSizePolicy, QComboBox,
)
from PyQt6.QtCore import Qt

import i18n
from i18n import t
from styles import COLORS
from ui_dashboard import DashboardPage
from ui_robots    import RobotsPage
from ui_records   import RecordsPage
from ui_inventory import InventoryPage


NAV_ITEMS = [
    ("nav_dashboard", "🏠"),
    ("nav_robots",    "🤖"),
    ("nav_records",   "📋"),
    ("nav_inventory", "📦"),
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(t("app_title"))
        self.setMinimumSize(1200, 750)
        self._setup_central()
        self._build_sidebar()
        self._build_content()
        self._nav_buttons[0].setProperty("active", "true")
        self._nav_buttons[0].style().unpolish(self._nav_buttons[0])
        self._nav_buttons[0].style().polish(self._nav_buttons[0])

    # ── Central widget ────────────────────────────────────────────────────────
    def _setup_central(self):
        central = QWidget()
        self._root_layout = QHBoxLayout(central)
        self._root_layout.setContentsMargins(0, 0, 0, 0)
        self._root_layout.setSpacing(0)
        self.setCentralWidget(central)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        self._sidebar = QWidget()
        self._sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(self._sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Logo
        logo = QLabel("🐝  BeePower")
        logo.setObjectName("logo_label")
        ver  = QLabel("Stok Takip Sistemi v1.0")
        ver.setObjectName("version_label")
        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(ver)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {COLORS['border']};")
        sidebar_layout.addWidget(sep)
        sidebar_layout.addSpacing(8)

        # Nav buttons
        self._nav_buttons: list[QPushButton] = []
        for key, icon in NAV_ITEMS:
            btn = QPushButton(f"  {icon}   {t(key)}")
            btn.setObjectName("nav_btn")
            btn.setCheckable(False)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setFixedHeight(46)
            idx = len(self._nav_buttons)
            btn.clicked.connect(lambda _, i=idx: self._navigate(i))
            self._nav_buttons.append(btn)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Language selector
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet(f"color: {COLORS['border']};")
        sidebar_layout.addWidget(sep2)

        lang_widget = QWidget()
        lang_layout = QHBoxLayout(lang_widget)
        lang_layout.setContentsMargins(12, 8, 12, 8)
        lang_lbl = QLabel(t("language") + ":")
        lang_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        self._lang_combo = QComboBox()
        self._lang_combo.addItem("🇹🇷 TR", "tr")
        self._lang_combo.addItem("🇬🇧 EN", "en")
        self._lang_combo.currentIndexChanged.connect(self._change_language)
        self._lang_combo.setFixedHeight(28)
        lang_layout.addWidget(lang_lbl)
        lang_layout.addWidget(self._lang_combo)
        sidebar_layout.addWidget(lang_widget)

        self._root_layout.addWidget(self._sidebar)

    # ── Content stack ─────────────────────────────────────────────────────────
    def _build_content(self):
        self._stack = QStackedWidget()
        self._stack.setObjectName("content_area")

        self._page_dashboard = DashboardPage()
        self._page_robots    = RobotsPage()
        self._page_records   = RecordsPage()
        self._page_inventory = InventoryPage()

        # Cross-page refresh wiring
        self._page_robots.robots_changed.connect(self._page_records.refresh)
        self._page_robots.robots_changed.connect(self._page_dashboard.refresh)
        self._page_inventory.refresh  # inventory changes trigger nothing extra yet

        self._stack.addWidget(self._page_dashboard)
        self._stack.addWidget(self._page_robots)
        self._stack.addWidget(self._page_records)
        self._stack.addWidget(self._page_inventory)

        self._root_layout.addWidget(self._stack, 1)

    # ── Navigation ────────────────────────────────────────────────────────────
    def _navigate(self, index: int):
        self._stack.setCurrentIndex(index)
        for i, btn in enumerate(self._nav_buttons):
            active = "true" if i == index else "false"
            btn.setProperty("active", active)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # Refresh the target page
        pages = [
            self._page_dashboard,
            self._page_robots,
            self._page_records,
            self._page_inventory,
        ]
        if hasattr(pages[index], "refresh"):
            pages[index].refresh()

    # ── Language switch ────────────────────────────────────────────────────────
    def _change_language(self):
        lang = self._lang_combo.currentData()
        i18n.set_language(lang)
        self._retranslate()

    def _retranslate(self):
        """Update all visible text after language change (lightweight re-render)."""
        self.setWindowTitle(t("app_title"))
        for idx, (key, icon) in enumerate(NAV_ITEMS):
            self._nav_buttons[idx].setText(f"  {icon}   {t(key)}")
        # Rebuild pages (simplest approach for now)
        self._page_records.refresh()
        self._page_inventory.refresh()
        self._page_robots.refresh()
        self._page_dashboard.refresh()
