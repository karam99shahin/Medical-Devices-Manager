import datetime
import csv

# ---------------------- Devices List ----------------------

devices = []


# ---------------------- Validation Helpers ----------------------

def is_id_exists(device_id):
    for device in devices:
        if device["id"] == device_id:
            return True
    return False


def is_valid_date(date_text):
    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_status(status):
    return status in ["ok", "warning", "error"]


# ---------------------- Core Functions ----------------------

def add_device(name, device_id, device_type, maintenance_date):
    """Add a new device to the list. Returns (success: bool, message: str)."""

    if is_id_exists(device_id):
        return False, "Device ID already exists"

    if not is_valid_date(maintenance_date):
        return False, "Invalid date format (use YYYY-MM-DD)"

    device = {
        "name": name,
        "id": device_id,
        "type": device_type,
        "status": "ok",
        "maintenance_date": maintenance_date
    }

    devices.append(device)
    return True, "Device added successfully"


def update_status(device_id, new_status):
    """Update the status of a device. Returns (success: bool, message: str)."""

    if not is_valid_status(new_status):
        return False, "Invalid status (must be ok, warning, or error)"

    for device in devices:
        if device["id"] == device_id:
            device["status"] = new_status

            with open("log.txt", "a") as log_file:
                log_file.write(
                    f"{datetime.datetime.now()} | Device ID:{device_id} | New Status: {new_status}\n"
                )
            return True, "Status updated successfully"

    return False, "Device not found"


def delete_device(device_id):
    """Delete a device by ID. Returns (success: bool, message: str)."""

    for device in devices:
        if device["id"] == device_id:
            devices.remove(device)
            return True, "Device deleted successfully"

    return False, "Device not found"





def find_device(device_id):
    """Return device dict if found, else None."""

    for device in devices:
        if device["id"] == device_id:
            return device

    return None

def find_devices_by_name(name_query):
    """Return a list of devices whose name contains the search query (case-insensitive)."""

    results = []

    for device in devices:
        if name_query.lower() in device["name"].lower():
            results.append(device)

    return results


def save_to_csv(filename):
    """Save all devices to a CSV file."""

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "id", "type", "status", "maintenance_date"])

        for device in devices:
            writer.writerow([
                device["name"],
                device["id"],
                device["type"],
                device["status"],
                device["maintenance_date"]
            ])


def load_from_csv(filename):
    """Load devices from a CSV file. Returns (success: bool, message: str)."""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header

            loaded_devices = []
            for row in reader:
                if len(row) < 5:
                    continue

                device = {
                    "name": row[0],
                    "id": row[1],
                    "type": row[2],
                    "status": row[3],
                    "maintenance_date": row[4]
                }
                loaded_devices.append(device)

        devices.clear()
        devices.extend(loaded_devices)
        return True, "Devices loaded successfully"

    except Exception:
        return False, "Failed to load file. Make sure it's a valid CSV export from this app."