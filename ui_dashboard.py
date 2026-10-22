"""
BeePower Stok Takip Sistemi - Dashboard Paneli
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy,
    QGridLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

import database as db
from i18n import t
from styles import COLORS


class StatCard(QWidget):
    def __init__(self, label: str, value: str, color: str = COLORS["accent"], parent=None):
        super().__init__(parent)
        self.setObjectName("stat_card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(4)

        self.value_lbl = QLabel(str(value))
        self.value_lbl.setObjectName("stat_value")
        self.value_lbl.setStyleSheet(f"color: {color}; font-size: 36px; font-weight: 700;")
        self.value_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_lbl = QLabel(label)
        self.label_lbl.setObjectName("stat_label")

        layout.addWidget(self.value_lbl)
        layout.addWidget(self.label_lbl)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def update_value(self, value: str):
        self.value_lbl.setText(str(value))

    def update_label(self, label: str):
        self.label_lbl.setText(label)


class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # ── Header ──────────────────────────────────────────────
        title = QLabel(t("dash_title"))
        title.setObjectName("page_title")
        layout.addWidget(title)

        # ── Stat cards ───────────────────────────────────────────
        grid = QGridLayout()
        grid.setSpacing(16)

        self.card_robots    = StatCard(t("dash_total_robots"),   "0", COLORS["accent"])
        self.card_records   = StatCard(t("dash_total_records"),  "0", COLORS["blue"])
        self.card_modules   = StatCard(t("dash_total_modules"),  "0", COLORS["text_secondary"])
        self.card_available = StatCard(t("dash_available"),      "0", COLORS["status_available"])
        self.card_faulty    = StatCard(t("dash_faulty"),         "0", COLORS["status_faulty"])
        self.card_unusable  = StatCard(t("dash_unusable"),       "0", COLORS["status_unusable"])

        grid.addWidget(self.card_robots,    0, 0)
        grid.addWidget(self.card_records,   0, 1)
        grid.addWidget(self.card_modules,   0, 2)
        grid.addWidget(self.card_available, 1, 0)
        grid.addWidget(self.card_faulty,    1, 1)
        grid.addWidget(self.card_unusable,  1, 2)

        layout.addLayout(grid)

        # ── Recent records table ─────────────────────────────────
        recent_lbl = QLabel(t("dash_recent"))
        recent_lbl.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {COLORS['text_primary']};")
        layout.addWidget(recent_lbl)

        self.recent_table = QTableWidget()
        self.recent_table.setAlternatingRowColors(True)
        self.recent_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.recent_table.verticalHeader().setVisible(False)
        self.recent_table.setColumnCount(6)
        self.recent_table.setHorizontalHeaderLabels([
            t("record_date"), t("record_robot"), t("record_module_cat"),
            t("record_reason"), t("record_solution"), t("record_status"),
        ])
        hdr = self.recent_table.horizontalHeader()
        hdr.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.recent_table.setMaximumHeight(280)
        layout.addWidget(self.recent_table)

        layout.addStretch()

    def refresh(self):
        stats = db.get_dashboard_stats()
        self.card_robots.update_value(str(stats["total_robots"]))
        self.card_records.update_value(str(stats["total_records"]))
        self.card_modules.update_value(str(stats["total_modules"]))
        self.card_available.update_value(str(stats["available_count"]))
        self.card_faulty.update_value(str(stats["faulty_count"]))
        self.card_unusable.update_value(str(stats["unusable_count"]))

        self.recent_table.setRowCount(0)
        status_colors = {
            "completed":   COLORS["status_available"],
            "pending":     COLORS["status_faulty"],
            "in_progress": COLORS["blue"],
        }
        status_labels = {
            "completed":   lambda: t("record_status_completed"),
            "pending":     lambda: t("record_status_pending"),
            "in_progress": lambda: t("record_status_in_progress"),
        }
        for rec in stats["recent_records"]:
            row = self.recent_table.rowCount()
            self.recent_table.insertRow(row)

            date_str = rec.get("record_date", "") or ""
            try:
                p = date_str.split("-")
                date_str = f"{p[2]}.{p[1]}.{p[0]}"
            except Exception:
                pass

            vals = [
                date_str,
                rec.get("robot_name", ""),
                rec.get("module_category", "") or "",
                rec.get("reason", "") or "",
                rec.get("solution", "") or "",
                status_labels.get(rec.get("status", ""), lambda: "")(),
            ]
            for col, val in enumerate(vals):
                cell = QTableWidgetItem(str(val))
                if col == 5:
                    color = status_colors.get(rec.get("status", ""), "#fff")
                    cell.setForeground(QColor(color))
                    cell.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
                self.recent_table.setItem(row, col, cell)
            self.recent_table.setRowHeight(row, 40)
