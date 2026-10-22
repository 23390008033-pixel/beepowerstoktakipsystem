"""
BeePower Stok Takip Sistemi - Çeviri Sistemi (TR/EN)
Internationalization module
"""

TRANSLATIONS = {
    "tr": {
        # App
        "app_title": "BeePower Stok Takip Sistemi",
        "language": "Dil",
        "turkish": "Türkçe",
        "english": "İngilizce",

        # Navigation
        "nav_dashboard": "Dashboard",
        "nav_records": "Kayıtlar",
        "nav_inventory": "Stok",
        "nav_robots": "Robotlar",

        # Dashboard
        "dash_title": "Genel Bakış",
        "dash_total_robots": "Toplam Robot",
        "dash_total_records": "Toplam Kayıt",
        "dash_total_modules": "Toplam Modül",
        "dash_available": "Kullanılabilir",
        "dash_faulty": "Sorunlu",
        "dash_unusable": "Kullanılamaz",
        "dash_recent": "Son Kayıtlar",

        # Robots
        "robots_title": "Robot Yönetimi",
        "robot_name": "Robot Adı",
        "robot_model": "Robot Modeli",
        "robot_serial": "Seri No",
        "robot_description": "Açıklama",
        "robot_add": "Robot Ekle",
        "robot_edit": "Robot Düzenle",
        "robot_delete": "Robot Sil",
        "robot_created": "Oluşturulma Tarihi",

        # Records
        "records_title": "Bakım / Değişim Kayıtları",
        "record_add": "Kayıt Ekle",
        "record_edit": "Kayıt Düzenle",
        "record_delete": "Kayıt Sil",
        "record_robot": "Robot",
        "record_module_cat": "Modül Kategorisi",
        "record_old_module_id": "Çıkarılan Modül ID",
        "record_old_module_name": "Çıkarılan Modül Adı",
        "record_reason": "Neden",
        "record_solution": "Çözüm",
        "record_new_module_id": "Takılan Modül ID",
        "record_date": "Tarih",
        "record_technician": "Teknisyen",
        "record_duration": "Süre (dk)",
        "record_cost": "Maliyet (₺)",
        "record_description": "Açıklama",
        "record_status": "Durum",
        "record_status_completed": "Tamamlandı",
        "record_status_pending": "Beklemede",
        "record_status_in_progress": "Devam Ediyor",

        # Inventory
        "inv_title": "Stok Yönetimi",
        "inv_add": "Modül Ekle",
        "inv_edit": "Modül Düzenle",
        "inv_delete": "Modül Sil",
        "inv_module_id": "Modül ID",
        "inv_name": "Modül Adı",
        "inv_category": "Kategori",
        "inv_quantity": "Adet",
        "inv_status": "Durum",
        "inv_description": "Açıklama",
        "inv_supplier": "Tedarikçi",
        "inv_cost": "Birim Maliyet (₺)",
        "inv_location": "Konum / Raf",
        "inv_available": "Kullanılabilir",
        "inv_faulty": "Sorunlu",
        "inv_unusable": "Kullanılamaz",
        "inv_all": "Tümü",
        "inv_move_available": "Kullanılabilire Taşı",
        "inv_move_faulty": "Sorunluya Taşı",
        "inv_move_unusable": "Kullanılamazı Taşı",

        # Common
        "btn_save": "Kaydet",
        "btn_cancel": "İptal",
        "btn_close": "Kapat",
        "btn_delete": "Sil",
        "btn_edit": "Düzenle",
        "btn_add": "Ekle",
        "btn_search": "Ara",
        "btn_export": "Excel'e Aktar",
        "btn_refresh": "Yenile",
        "confirm_delete": "Silmek istediğinizden emin misiniz?",
        "confirm_title": "Onay",
        "error_title": "Hata",
        "success_title": "Başarılı",
        "warning_title": "Uyarı",
        "field_required": "Bu alan zorunludur.",
        "search_placeholder": "Ara...",
        "no_data": "Veri bulunamadı.",
        "updated_at": "Güncellenme Tarihi",
        "created_at": "Oluşturulma Tarihi",
        "select": "Seçiniz...",
        "total": "Toplam",
        "filter": "Filtre",
        "all": "Tümü",
    },

    "en": {
        # App
        "app_title": "BeePower Stock Tracking System",
        "language": "Language",
        "turkish": "Turkish",
        "english": "English",

        # Navigation
        "nav_dashboard": "Dashboard",
        "nav_records": "Records",
        "nav_inventory": "Inventory",
        "nav_robots": "Robots",

        # Dashboard
        "dash_title": "Overview",
        "dash_total_robots": "Total Robots",
        "dash_total_records": "Total Records",
        "dash_total_modules": "Total Modules",
        "dash_available": "Available",
        "dash_faulty": "Faulty",
        "dash_unusable": "Unusable",
        "dash_recent": "Recent Records",

        # Robots
        "robots_title": "Robot Management",
        "robot_name": "Robot Name",
        "robot_model": "Robot Model",
        "robot_serial": "Serial No",
        "robot_description": "Description",
        "robot_add": "Add Robot",
        "robot_edit": "Edit Robot",
        "robot_delete": "Delete Robot",
        "robot_created": "Created At",

        # Records
        "records_title": "Maintenance / Change Records",
        "record_add": "Add Record",
        "record_edit": "Edit Record",
        "record_delete": "Delete Record",
        "record_robot": "Robot",
        "record_module_cat": "Module Category",
        "record_old_module_id": "Removed Module ID",
        "record_old_module_name": "Removed Module Name",
        "record_reason": "Reason",
        "record_solution": "Solution",
        "record_new_module_id": "Installed Module ID",
        "record_date": "Date",
        "record_technician": "Technician",
        "record_duration": "Duration (min)",
        "record_cost": "Cost (₺)",
        "record_description": "Description",
        "record_status": "Status",
        "record_status_completed": "Completed",
        "record_status_pending": "Pending",
        "record_status_in_progress": "In Progress",

        # Inventory
        "inv_title": "Inventory Management",
        "inv_add": "Add Module",
        "inv_edit": "Edit Module",
        "inv_delete": "Delete Module",
        "inv_module_id": "Module ID",
        "inv_name": "Module Name",
        "inv_category": "Category",
        "inv_quantity": "Quantity",
        "inv_status": "Status",
        "inv_description": "Description",
        "inv_supplier": "Supplier",
        "inv_cost": "Unit Cost (₺)",
        "inv_location": "Location / Shelf",
        "inv_available": "Available",
        "inv_faulty": "Faulty",
        "inv_unusable": "Unusable",
        "inv_all": "All",
        "inv_move_available": "Move to Available",
        "inv_move_faulty": "Move to Faulty",
        "inv_move_unusable": "Move to Unusable",

        # Common
        "btn_save": "Save",
        "btn_cancel": "Cancel",
        "btn_close": "Close",
        "btn_delete": "Delete",
        "btn_edit": "Edit",
        "btn_add": "Add",
        "btn_search": "Search",
        "btn_export": "Export to Excel",
        "btn_refresh": "Refresh",
        "confirm_delete": "Are you sure you want to delete?",
        "confirm_title": "Confirm",
        "error_title": "Error",
        "success_title": "Success",
        "warning_title": "Warning",
        "field_required": "This field is required.",
        "search_placeholder": "Search...",
        "no_data": "No data found.",
        "updated_at": "Updated At",
        "created_at": "Created At",
        "select": "Select...",
        "total": "Total",
        "filter": "Filter",
        "all": "All",
    },
}

_current_lang = "tr"


def set_language(lang: str):
    global _current_lang
    if lang in TRANSLATIONS:
        _current_lang = lang


def get_language() -> str:
    return _current_lang


def t(key: str) -> str:
    """Translate a key to the current language."""
    return TRANSLATIONS.get(_current_lang, TRANSLATIONS["tr"]).get(key, key)
