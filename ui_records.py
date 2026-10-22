"""
BeePower Stok Takip Sistemi - Kayıt (Bakım/Değişim) Paneli
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QDialog, QFormLayout, QTextEdit, QMessageBox, QComboBox,
    QSpinBox, QDoubleSpinBox, QDateEdit, QFrame, QCompleter,
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont

import database as db
from i18n import t
from styles import COLORS


STATUS_COLORS = {
    "completed":   COLORS["status_available"],
    "pending":     COLORS["status_faulty"],
    "in_progress": COLORS["blue"],
}


def _status_label(s: str) -> str:
    mapping = {
        "completed":   lambda: t("record_status_completed"),
        "pending":     lambda: t("record_status_pending"),
        "in_progress": lambda: t("record_status_in_progress"),
    }
    return mapping.get(s, lambda: s)()


class RecordDialog(QDialog):
    """Add / Edit maintenance record dialog."""

    def __init__(self, parent=None, record: dict | None = None):
        super().__init__(parent)
        self.record = record
        self._robots     = db.get_all_robots()
        self._categories = db.get_all_categories()
        self._inventory  = db.get_all_inventory("available")
        self._build_ui()
        if record:
            self._populate(record)

    # ── Build ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        self.setWindowTitle(t("record_edit") if self.record else t("record_add"))
        self.setMinimumWidth(560)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel(t("record_edit") if self.record else t("record_add"))
        title.setObjectName("dialog_title")
        layout.addWidget(title)
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        def lbl(key):
            l = QLabel(t(key))
            l.setObjectName("form_label")
            return l

        # Robot
        self.robot_combo = QComboBox()
        self.robot_combo.addItem(t("select"), None)
        for r in self._robots:
            self.robot_combo.addItem(r["name"], r["id"])
        form.addRow(lbl("record_robot"), self.robot_combo)

        # Module category
        self.cat_combo = QComboBox()
        self.cat_combo.addItem(t("select"), None)
        for c in self._categories:
            self.cat_combo.addItem(c["name"], c["id"])
        form.addRow(lbl("record_module_cat"), self.cat_combo)

        # Removed module (ID + name)
        self.old_id_edit = QLineEdit()
        self.old_id_edit.setPlaceholderText("57679")
        form.addRow(lbl("record_old_module_id"), self.old_id_edit)

        self.old_name_edit = QLineEdit()
        self.old_name_edit.setPlaceholderText("Tekerlek, Hub Motor, ...")
        form.addRow(lbl("record_old_module_name"), self.old_name_edit)

        # Reason
        self.reason_edit = QLineEdit()
        self.reason_edit.setPlaceholderText("Arıza, aşınma, ...")
        form.addRow(lbl("record_reason"), self.reason_edit)

        # Solution
        self.solution_edit = QLineEdit()
        self.solution_edit.setPlaceholderText("Yeni modül takıldı, tamir edildi, ...")
        form.addRow(lbl("record_solution"), self.solution_edit)

        # New module ID (with autocomplete from available inventory)
        new_mod_row = QHBoxLayout()
        self.new_id_edit = QLineEdit()
        self.new_id_edit.setPlaceholderText("Stoktan seç veya yaz...")
        inv_ids   = [i["module_id"] for i in self._inventory]
        inv_names = [f"{i['module_id']} — {i['name']}" for i in self._inventory]
        completer = QCompleter(inv_names, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.activated.connect(self._on_completer_activated)
        self.new_id_edit.setCompleter(completer)
        self._completer_inv = self._inventory  # keep ref

        # Quick-pick combo
        self.new_id_combo = QComboBox()
        self.new_id_combo.addItem("—", "")
        for i in self._inventory:
            self.new_id_combo.addItem(f"{i['module_id']}  {i['name']}  (Adet: {i['quantity']})", i["module_id"])
        self.new_id_combo.currentIndexChanged.connect(self._on_combo_pick)

        new_mod_row.addWidget(self.new_id_edit, 2)
        new_mod_row.addWidget(self.new_id_combo, 3)
        form.addRow(lbl("record_new_module_id"), new_mod_row)

        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        form.addRow(lbl("record_date"), self.date_edit)

        # Technician
        self.tech_edit = QLineEdit()
        form.addRow(lbl("record_technician"), self.tech_edit)

        # Duration & cost (same row)
        dur_cost = QHBoxLayout()
        self.dur_spin = QSpinBox()
        self.dur_spin.setRange(0, 99999)
        self.dur_spin.setSuffix(" dk")
        self.cost_spin = QDoubleSpinBox()
        self.cost_spin.setRange(0, 9999999)
        self.cost_spin.setDecimals(2)
        self.cost_spin.setSuffix(" ₺")
        lbl_dur  = QLabel(t("record_duration")); lbl_dur.setObjectName("form_label")
        lbl_cost = QLabel(t("record_cost"));     lbl_cost.setObjectName("form_label")
        dur_cost.addWidget(lbl_dur); dur_cost.addWidget(self.dur_spin)
        dur_cost.addSpacing(12)
        dur_cost.addWidget(lbl_cost); dur_cost.addWidget(self.cost_spin)
        form.addRow(QLabel(""), dur_cost)

        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItem(t("record_status_completed"),   "completed")
        self.status_combo.addItem(t("record_status_pending"),     "pending")
        self.status_combo.addItem(t("record_status_in_progress"), "in_progress")
        form.addRow(lbl("record_status"), self.status_combo)

        # Description
        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(72)
        self.desc_edit.setPlaceholderText("Zemin düzensizliğinden dolayı aşırı titreşim...")
        form.addRow(lbl("record_description"), self.desc_edit)

        layout.addLayout(form)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_c = QPushButton(t("btn_cancel"))
        btn_c.setObjectName("btn_secondary")
        btn_c.clicked.connect(self.reject)
        btn_s = QPushButton(t("btn_save"))
        btn_s.clicked.connect(self._save)
        btn_row.addWidget(btn_c)
        btn_row.addWidget(btn_s)
        layout.addLayout(btn_row)

    # ── Autocomplete helpers ──────────────────────────────────────────────────
    def _on_completer_activated(self, text: str):
        """Fill the ID field when user picks from completer list."""
        if "—" in text:
            mid = text.split("—")[0].strip()
            self.new_id_edit.setText(mid)

    def _on_combo_pick(self, index: int):
        mid = self.new_id_combo.itemData(index)
        if mid:
            self.new_id_edit.setText(mid)

    # ── Populate for edit ─────────────────────────────────────────────────────
    def _populate(self, r: dict):
        for i in range(self.robot_combo.count()):
            if self.robot_combo.itemData(i) == r.get("robot_id"):
                self.robot_combo.setCurrentIndex(i); break
        cat_name = r.get("module_category", "")
        for i in range(self.cat_combo.count()):
            if self.cat_combo.itemText(i) == cat_name:
                self.cat_combo.setCurrentIndex(i); break
        self.old_id_edit.setText(r.get("old_module_id", "") or "")
        self.old_name_edit.setText(r.get("old_module_name", "") or "")
        self.reason_edit.setText(r.get("reason", "") or "")
        self.solution_edit.setText(r.get("solution", "") or "")
        self.new_id_edit.setText(r.get("new_module_id", "") or "")
        date_str = r.get("record_date", "") or ""
        if date_str:
            try:
                parts = date_str.split("-")
                self.date_edit.setDate(QDate(int(parts[0]), int(parts[1]), int(parts[2])))
            except Exception:
                pass
        self.tech_edit.setText(r.get("technician", "") or "")
        self.dur_spin.setValue(r.get("duration_minutes") or 0)
        self.cost_spin.setValue(r.get("cost") or 0.0)
        status = r.get("status", "completed")
        for i in range(self.status_combo.count()):
            if self.status_combo.itemData(i) == status:
                self.status_combo.setCurrentIndex(i); break
        self.desc_edit.setPlainText(r.get("description", "") or "")

    # ── Save ──────────────────────────────────────────────────────────────────
    def _save(self):
        robot_id = self.robot_combo.currentData()
        reason   = self.reason_edit.text().strip()
        solution = self.solution_edit.text().strip()
        if not robot_id:
            QMessageBox.warning(self, t("warning_title"), t("record_robot") + " " + t("field_required"))
            return
        if not reason:
            QMessageBox.warning(self, t("warning_title"), t("record_reason") + " " + t("field_required"))
            return
        if not solution:
            QMessageBox.warning(self, t("warning_title"), t("record_solution") + " " + t("field_required"))
            return

        cat_text    = self.cat_combo.currentText() if self.cat_combo.currentData() else ""
        old_mod_id  = self.old_id_edit.text().strip()
        old_mod_nm  = self.old_name_edit.text().strip()
        new_mod_id  = self.new_id_edit.text().strip()
        rec_date    = self.date_edit.date().toString("yyyy-MM-dd")
        tech        = self.tech_edit.text().strip()
        dur         = self.dur_spin.value() or None
        cost        = self.cost_spin.value() or None
        status      = self.status_combo.currentData()
        desc        = self.desc_edit.toPlainText().strip()

        try:
            if self.record:
                db.update_record(
                    self.record["id"], robot_id, cat_text, old_mod_id, old_mod_nm,
                    reason, solution, new_mod_id, rec_date, tech, dur, cost, desc, status,
                )
            else:
                db.add_record(
                    robot_id, cat_text, old_mod_id, old_mod_nm,
                    reason, solution, new_mod_id, rec_date, tech, dur, cost, desc, status,
                )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, t("error_title"), str(e))


class RecordsPage(QWidget):
    """Maintenance / change records page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # ── Header ─────────────────────────────────────────────
        hdr = QHBoxLayout()
        title = QLabel(t("records_title"))
        title.setObjectName("page_title")
        hdr.addWidget(title)
        hdr.addStretch()

        # Robot filter
        self.robot_filter = QComboBox()
        self.robot_filter.setMinimumWidth(140)
        self.robot_filter.addItem(t("all"), None)
        for r in db.get_all_robots():
            self.robot_filter.addItem(r["name"], r["id"])
        self.robot_filter.currentIndexChanged.connect(self._apply_filter)
        hdr.addWidget(QLabel(t("record_robot") + ":"))
        hdr.addWidget(self.robot_filter)

        self.search_edit = QLineEdit()
        self.search_edit.setObjectName("search_bar")
        self.search_edit.setPlaceholderText(t("search_placeholder"))
        self.search_edit.textChanged.connect(self._search)
        hdr.addWidget(self.search_edit)

        btn_add = QPushButton(f"＋  {t('record_add')}")
        btn_add.clicked.connect(self._add)
        hdr.addWidget(btn_add)

        layout.addLayout(hdr)

        # ── Record count ───────────────────────────────────────
        self.count_lbl = QLabel()
        self.count_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        layout.addWidget(self.count_lbl)

        # ── Table ──────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        cols = [
            t("record_date"), t("record_robot"), t("record_module_cat"),
            t("record_old_module_id"), t("record_old_module_name"),
            t("record_reason"), t("record_solution"), t("record_new_module_id"),
            t("record_technician"), t("record_status"), "Actions",
        ]
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        hdr_v = self.table.horizontalHeader()
        hdr_v.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        hdr_v.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        hdr_v.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

    def refresh(self):
        # Refresh robot filter list
        current_robot = self.robot_filter.currentData()
        self.robot_filter.blockSignals(True)
        self.robot_filter.clear()
        self.robot_filter.addItem(t("all"), None)
        for r in db.get_all_robots():
            self.robot_filter.addItem(r["name"], r["id"])
        # restore selection
        for i in range(self.robot_filter.count()):
            if self.robot_filter.itemData(i) == current_robot:
                self.robot_filter.setCurrentIndex(i); break
        self.robot_filter.blockSignals(False)
        self._apply_filter()

    def _apply_filter(self):
        robot_id = self.robot_filter.currentData()
        records  = db.get_all_records(robot_id)
        self._populate(records)

    def _search(self, text: str):
        if not text.strip():
            self._apply_filter()
            return
        records = db.search_records(text.strip())
        self._populate(records)

    def _populate(self, records: list[dict]):
        self.table.setRowCount(0)
        self.count_lbl.setText(f"{t('total')}: {len(records)}")
        for rec in records:
            row = self.table.rowCount()
            self.table.insertRow(row)

            date_str = (rec.get("record_date") or "")
            try:
                parts = date_str.split("-")
                date_str = f"{parts[2]}.{parts[1]}.{parts[0]}"
            except Exception:
                pass

            values = [
                date_str,
                rec.get("robot_name", ""),
                rec.get("module_category", "") or "",
                rec.get("old_module_id", "") or "",
                rec.get("old_module_name", "") or "",
                rec.get("reason", "") or "",
                rec.get("solution", "") or "",
                rec.get("new_module_id", "") or "",
                rec.get("technician", "") or "",
                _status_label(rec.get("status", "completed")),
            ]
            for col, val in enumerate(values):
                cell = QTableWidgetItem(str(val))
                if col == 9:  # status
                    color = STATUS_COLORS.get(rec.get("status", ""), "#fff")
                    cell.setForeground(QColor(color))
                    cell.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
                self.table.setItem(row, col, cell)

            # Action buttons
            aw = QWidget()
            al = QHBoxLayout(aw)
            al.setContentsMargins(4, 2, 4, 2)
            al.setSpacing(4)

            btn_e = QPushButton(t("btn_edit"))
            btn_e.setObjectName("btn_secondary")
            btn_e.setFixedHeight(26)
            btn_e.clicked.connect(lambda _, r=rec: self._edit(r))

            btn_d = QPushButton(t("btn_delete"))
            btn_d.setObjectName("btn_danger")
            btn_d.setFixedHeight(26)
            btn_d.clicked.connect(lambda _, r=rec: self._delete(r))

            al.addWidget(btn_e)
            al.addWidget(btn_d)
            self.table.setCellWidget(row, len(values), aw)
            self.table.setRowHeight(row, 44)

    def _add(self):
        dlg = RecordDialog(self)
        if dlg.exec():
            self.refresh()

    def _edit(self, rec: dict):
        dlg = RecordDialog(self, rec)
        if dlg.exec():
            self.refresh()

    def _delete(self, rec: dict):
        reply = QMessageBox.question(
            self, t("confirm_title"), t("confirm_delete"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            db.delete_record(rec["id"])
            self.refresh()
