"""
BeePower Stok Takip Sistemi - Stok / Envanter Paneli
"""
from __future__ import annotations


from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QDialog, QFormLayout, QTextEdit, QMessageBox, QComboBox,
    QSpinBox, QDoubleSpinBox, QTabWidget, QFrame, QMenu,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QAction


import database as db
from i18n import t
from styles import COLORS


STATUS_LABELS = {
    "available": lambda: t("inv_available"),
    "faulty":    lambda: t("inv_faulty"),
    "unusable":  lambda: t("inv_unusable"),
}
STATUS_COLORS = {
    "available": COLORS["status_available"],
    "faulty":    COLORS["status_faulty"],
    "unusable":  COLORS["status_unusable"],
}


class InventoryDialog(QDialog):
    """Add / Edit module dialog."""

    def __init__(self, parent=None, item: dict | None = None):
        super().__init__(parent)
        self.item = item
        self._categories = db.get_all_categories()
        self._build_ui()
        if item:
            self._populate(item)

    def _build_ui(self):
        self.setWindowTitle(t("inv_edit") if self.item else t("inv_add"))
        self.setMinimumWidth(480)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel(t("inv_edit") if self.item else t("inv_add"))
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

        self.mod_id_edit = QLineEdit()
        self.mod_id_edit.setPlaceholderText("57681")
        form.addRow(lbl("inv_module_id"), self.mod_id_edit)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Hub Motor, Tekerlek, ...")
        form.addRow(lbl("inv_name"), self.name_edit)

        self.cat_combo = QComboBox()
        self.cat_combo.addItem(t("select"), None)
        for cat in self._categories:
            self.cat_combo.addItem(cat["name"], cat["id"])
        form.addRow(lbl("inv_category"), self.cat_combo)

        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(0, 99999)
        form.addRow(lbl("inv_quantity"), self.qty_spin)

        self.status_combo = QComboBox()
        self.status_combo.addItem(t("inv_available"), "available")
        self.status_combo.addItem(t("inv_faulty"),    "faulty")
        self.status_combo.addItem(t("inv_unusable"),  "unusable")
        form.addRow(lbl("inv_status"), self.status_combo)

        self.supplier_edit = QLineEdit()
        form.addRow(lbl("inv_supplier"), self.supplier_edit)

        self.cost_spin = QDoubleSpinBox()
        self.cost_spin.setRange(0, 9999999)
        self.cost_spin.setDecimals(2)
        self.cost_spin.setSuffix(" ₺")
        form.addRow(lbl("inv_cost"), self.cost_spin)

        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("Raf A-3, ...")
        form.addRow(lbl("inv_location"), self.location_edit)

        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(72)
        form.addRow(lbl("inv_description"), self.desc_edit)

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

    def _populate(self, item: dict):
        self.mod_id_edit.setText(item.get("module_id", ""))
        self.name_edit.setText(item.get("name", ""))
        # category
        cat_id = item.get("category_id")
        for i in range(self.cat_combo.count()):
            if self.cat_combo.itemData(i) == cat_id:
                self.cat_combo.setCurrentIndex(i)
                break
        self.qty_spin.setValue(item.get("quantity", 0))
        status = item.get("status", "available")
        for i in range(self.status_combo.count()):
            if self.status_combo.itemData(i) == status:
                self.status_combo.setCurrentIndex(i)
                break
        self.supplier_edit.setText(item.get("supplier", "") or "")
        self.cost_spin.setValue(item.get("unit_cost") or 0.0)
        self.location_edit.setText(item.get("location", "") or "")
        self.desc_edit.setPlainText(item.get("description", "") or "")

    def _save(self):
        mod_id = self.mod_id_edit.text().strip()
        name   = self.name_edit.text().strip()
        if not mod_id or not name:
            QMessageBox.warning(self, t("warning_title"), t("field_required"))
            return
        cat_id   = self.cat_combo.currentData()
        qty      = self.qty_spin.value()
        status   = self.status_combo.currentData()
        supplier = self.supplier_edit.text().strip()
        cost     = self.cost_spin.value() or None
        location = self.location_edit.text().strip()
        desc     = self.desc_edit.toPlainText().strip()
        try:
            if self.item:
                db.update_inventory(
                    self.item["id"], mod_id, name, cat_id, qty, status,
                    desc, supplier, cost, location,
                )
            else:
                db.add_inventory(mod_id, name, cat_id, qty, status, desc, supplier, cost, location)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, t("error_title"), str(e))


class InventoryTable(QTableWidget):
    """Reusable table for inventory items."""

    COLUMNS = [
        ("inv_module_id", "module_id"),
        ("inv_name",      "name"),
        ("inv_category",  "category_name"),
        ("inv_quantity",  "quantity"),
        ("inv_status",    "status"),
        ("inv_location",  "location"),
        ("inv_supplier",  "supplier"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.setColumnCount(len(self.COLUMNS) + 1)
        self._set_headers()
        hdr = self.horizontalHeader()
        hdr.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(len(self.COLUMNS), QHeaderView.ResizeMode.ResizeToContents)

    def _set_headers(self):
        headers = [t(c[0]) for c in self.COLUMNS] + ["Actions"]
        self.setHorizontalHeaderLabels(headers)

    def retranslate(self):
        self._set_headers()

    def populate(self, items: list[dict], edit_cb, delete_cb, move_cb):
        self.setRowCount(0)
        for item in items:
            row = self.rowCount()
            self.insertRow(row)
            for col, (_, key) in enumerate(self.COLUMNS):
                val = item.get(key, "") or ""
                cell = QTableWidgetItem(str(val))
                if key == "status":
                    color = STATUS_COLORS.get(str(val), "#fff")
                    cell.setForeground(QColor(color))
                    cell.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
                    cell.setText(STATUS_LABELS.get(str(val), lambda: str(val))())
                self.setItem(row, col, cell)

            # Actions
            aw = QWidget()
            al = QHBoxLayout(aw)
            al.setContentsMargins(4, 2, 4, 2)
            al.setSpacing(4)

            btn_e = QPushButton(t("btn_edit"))
            btn_e.setObjectName("btn_secondary")
            btn_e.setFixedHeight(26)
            btn_e.clicked.connect(lambda _, i=item: edit_cb(i))

            btn_m = QPushButton("⇄")
            btn_m.setObjectName("btn_warning")
            btn_m.setFixedHeight(26)
            btn_m.setFixedWidth(30)
            btn_m.setToolTip(t("filter"))
            btn_m.clicked.connect(lambda _, i=item: move_cb(btn_m, i))

            btn_d = QPushButton(t("btn_delete"))
            btn_d.setObjectName("btn_danger")
            btn_d.setFixedHeight(26)
            btn_d.clicked.connect(lambda _, i=item: delete_cb(i))

            al.addWidget(btn_e)
            al.addWidget(btn_m)
            al.addWidget(btn_d)
            self.setCellWidget(row, len(self.COLUMNS), aw)
            self.setRowHeight(row, 44)


class InventoryPage(QWidget):
    """Inventory management page with status tabs."""

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
        title = QLabel(t("inv_title"))
        title.setObjectName("page_title")
        hdr.addWidget(title)
        hdr.addStretch()

        self.search_edit = QLineEdit()
        self.search_edit.setObjectName("search_bar")
        self.search_edit.setPlaceholderText(t("search_placeholder"))
        self.search_edit.textChanged.connect(self._search)
        hdr.addWidget(self.search_edit)

        btn_add = QPushButton(f"＋  {t('inv_add')}")
        btn_add.clicked.connect(self._add)
        hdr.addWidget(btn_add)

        layout.addLayout(hdr)

        # ── Stats row ──────────────────────────────────────────
        self.stat_row = QHBoxLayout()
        self.lbl_total     = QLabel()
        self.lbl_available = QLabel()
        self.lbl_faulty    = QLabel()
        self.lbl_unusable  = QLabel()
        for lbl, color in [
            (self.lbl_total,     COLORS["text_secondary"]),
            (self.lbl_available, COLORS["status_available"]),
            (self.lbl_faulty,    COLORS["status_faulty"]),
            (self.lbl_unusable,  COLORS["status_unusable"]),
        ]:
            lbl.setStyleSheet(f"color: {color}; font-weight: 600; font-size: 12px;")
            self.stat_row.addWidget(lbl)
        self.stat_row.addStretch()
        layout.addLayout(self.stat_row)

        # ── Tabs ───────────────────────────────────────────────
        self.tabs = QTabWidget()

        self.tbl_all       = InventoryTable()
        self.tbl_available = InventoryTable()
        self.tbl_faulty    = InventoryTable()
        self.tbl_unusable  = InventoryTable()

        self.tabs.addTab(self.tbl_all,       t("inv_all"))
        self.tabs.addTab(self.tbl_available, t("inv_available"))
        self.tabs.addTab(self.tbl_faulty,    t("inv_faulty"))
        self.tabs.addTab(self.tbl_unusable,  t("inv_unusable"))

        layout.addWidget(self.tabs)

    def refresh(self):
        all_items       = db.get_all_inventory()
        available_items = db.get_all_inventory("available")
        faulty_items    = db.get_all_inventory("faulty")
        unusable_items  = db.get_all_inventory("unusable")

        self.tbl_all.populate(all_items,             self._edit, self._delete, self._move_menu)
        self.tbl_available.populate(available_items, self._edit, self._delete, self._move_menu)
        self.tbl_faulty.populate(faulty_items,       self._edit, self._delete, self._move_menu)
        self.tbl_unusable.populate(unusable_items,   self._edit, self._delete, self._move_menu)

        total = len(all_items)
        avail = len(available_items)
        fault = len(faulty_items)
        unus  = len(unusable_items)
        self.lbl_total.setText(f"  {t('total')}: {total}  ")
        self.lbl_available.setText(f"●  {t('inv_available')}: {avail}  ")
        self.lbl_faulty.setText(f"●  {t('inv_faulty')}: {fault}  ")
        self.lbl_unusable.setText(f"●  {t('inv_unusable')}: {unus}  ")

    def _search(self, text: str):
        if not text.strip():
            self.refresh()
            return
        items = db.search_inventory(text.strip())
        self.tbl_all.populate(items, self._edit, self._delete, self._move_menu)

    def _add(self):
        dlg = InventoryDialog(self)
        if dlg.exec():
            self.refresh()

    def _edit(self, item: dict):
        dlg = InventoryDialog(self, item)
        if dlg.exec():
            self.refresh()

    def _delete(self, item: dict):
        reply = QMessageBox.question(
            self, t("confirm_title"), t("confirm_delete"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            db.delete_inventory(item["id"])
            self.refresh()

    def _move_menu(self, button, item: dict):
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: #1e2235;
                color: #fff;
                border: 1px solid #2e3250;
                border-radius: 6px;
                padding: 4px;
            }}
            QMenu::item {{ padding: 8px 20px; border-radius: 4px; }}
            QMenu::item:selected {{ background-color: #2d3561; }}
        """)

        act_avail = QAction(t("inv_move_available"), self)
        act_fault = QAction(t("inv_move_faulty"),    self)
        act_unus  = QAction(t("inv_move_unusable"),  self)

        act_avail.triggered.connect(lambda: self._move(item, "available"))
        act_fault.triggered.connect(lambda: self._move(item, "faulty"))
        act_unus.triggered.connect(lambda:  self._move(item, "unusable"))

        menu.addAction(act_avail)
        menu.addAction(act_fault)
        menu.addAction(act_unus)
        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))

    def _move(self, item: dict, new_status: str):
        db.update_inventory_status(item["module_id"], new_status)
        self.refresh()
