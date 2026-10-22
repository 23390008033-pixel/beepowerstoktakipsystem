"""
BeePower Stok Takip Sistemi - Robot Yönetim Paneli
"""
from __future__ import annotations


from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QDialog, QFormLayout, QTextEdit, QMessageBox, QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal

import database as db
from i18n import t


class RobotDialog(QDialog):
    """Add / Edit robot dialog."""

    def __init__(self, parent=None, robot: dict | None = None):
        super().__init__(parent)
        self.robot = robot
        self._build_ui()
        if robot:
            self._populate(robot)

    def _build_ui(self):
        self.setWindowTitle(t("robot_edit") if self.robot else t("robot_add"))
        self.setMinimumWidth(440)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # Title
        title = QLabel(t("robot_edit") if self.robot else t("robot_add"))
        title.setObjectName("dialog_title")
        layout.addWidget(title)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        def lbl(key):
            l = QLabel(t(key))
            l.setObjectName("form_label")
            return l

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("B1, R2, ...")
        form.addRow(lbl("robot_name") , self.name_edit)

        self.model_edit = QLineEdit()
        self.model_edit.setPlaceholderText("BeeBot v2, ...")
        form.addRow(lbl("robot_model"), self.model_edit)

        self.serial_edit = QLineEdit()
        self.serial_edit.setPlaceholderText("SN-001")
        form.addRow(lbl("robot_serial"), self.serial_edit)

        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(80)
        form.addRow(lbl("robot_description"), self.desc_edit)

        layout.addLayout(form)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.btn_cancel = QPushButton(t("btn_cancel"))
        self.btn_cancel.setObjectName("btn_secondary")
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save = QPushButton(t("btn_save"))
        self.btn_save.clicked.connect(self._save)
        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_save)
        layout.addLayout(btn_row)

    def _populate(self, robot: dict):
        self.name_edit.setText(robot.get("name", ""))
        self.model_edit.setText(robot.get("model", "") or "")
        self.serial_edit.setText(robot.get("serial_no", "") or "")
        self.desc_edit.setPlainText(robot.get("description", "") or "")

    def _save(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, t("warning_title"), t("field_required"))
            return
        model   = self.model_edit.text().strip()
        serial  = self.serial_edit.text().strip()
        desc    = self.desc_edit.toPlainText().strip()

        try:
            if self.robot:
                db.update_robot(self.robot["id"], name, model, serial, desc)
            else:
                db.add_robot(name, model, serial, desc)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, t("error_title"), str(e))

    def get_data(self):
        return {
            "name":        self.name_edit.text().strip(),
            "model":       self.model_edit.text().strip(),
            "serial_no":   self.serial_edit.text().strip(),
            "description": self.desc_edit.toPlainText().strip(),
        }


class RobotsPage(QWidget):
    """Robot management page."""

    robots_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # ── Header ──────────────────────────────────────────────
        hdr = QHBoxLayout()
        title_col = QVBoxLayout()
        title = QLabel(t("robots_title"))
        title.setObjectName("page_title")
        sub = QLabel(t("robot_description"))
        sub.setObjectName("page_subtitle")
        title_col.addWidget(title)
        hdr.addLayout(title_col)
        hdr.addStretch()

        self.search_edit = QLineEdit()
        self.search_edit.setObjectName("search_bar")
        self.search_edit.setPlaceholderText(t("search_placeholder"))
        self.search_edit.textChanged.connect(self._filter)
        hdr.addWidget(self.search_edit)

        btn_add = QPushButton(f"＋  {t('robot_add')}")
        btn_add.clicked.connect(self._add)
        hdr.addWidget(btn_add)

        layout.addLayout(hdr)

        # ── Table ────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            t("robot_name"), t("robot_model"), t("robot_serial"),
            t("robot_description"), t("robot_created"), "Actions",
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.table)

        self._all_robots = []

    def refresh(self):
        self._all_robots = db.get_all_robots()
        self._populate(self._all_robots)
        self.robots_changed.emit()

    def _filter(self, text: str):
        q = text.lower()
        filtered = [r for r in self._all_robots if q in (r.get("name") or "").lower()
                    or q in (r.get("model") or "").lower()
                    or q in (r.get("serial_no") or "").lower()]
        self._populate(filtered)

    def _populate(self, robots: list[dict]):
        self.table.setRowCount(0)
        for robot in robots:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(robot.get("name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(robot.get("model", "") or ""))
            self.table.setItem(row, 2, QTableWidgetItem(robot.get("serial_no", "") or ""))
            self.table.setItem(row, 3, QTableWidgetItem(robot.get("description", "") or ""))
            self.table.setItem(row, 4, QTableWidgetItem((robot.get("created_at", "") or "")[:10]))

            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 2, 4, 2)
            action_layout.setSpacing(6)

            btn_edit = QPushButton(t("btn_edit"))
            btn_edit.setObjectName("btn_secondary")
            btn_edit.setFixedHeight(26)
            btn_edit.clicked.connect(lambda _, r=robot: self._edit(r))

            btn_del = QPushButton(t("btn_delete"))
            btn_del.setObjectName("btn_danger")
            btn_del.setFixedHeight(26)
            btn_del.clicked.connect(lambda _, r=robot: self._delete(r))

            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_del)
            self.table.setCellWidget(row, 5, action_widget)
            self.table.setRowHeight(row, 44)

    def _add(self):
        dlg = RobotDialog(self)
        if dlg.exec():
            self.refresh()

    def _edit(self, robot: dict):
        dlg = RobotDialog(self, robot)
        if dlg.exec():
            self.refresh()

    def _delete(self, robot: dict):
        reply = QMessageBox.question(
            self, t("confirm_title"), t("confirm_delete"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            db.delete_robot(robot["id"])
            self.refresh()
