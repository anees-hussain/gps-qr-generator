import qrcode
import os
import re
from datetime import datetime


def extract_lat_lng_from_url(url):
    """
    Tries to extract latitude & longitude from Google Maps URL.
    Returns (lat, lng) or (None, None)
    """
    # Pattern for !1d{lng}!2d{lat}
    match = re.search(r"!1d([0-9.]+)!2d([0-9.]+)", url)
    if match:
        lng, lat = match.groups()
        return lat, lng

    # Pattern for @lat,lng
    match = re.search(r"@([0-9.]+),([0-9.]+)", url)
    if match:
        lat, lng = match.groups()
        return lat, lng

    return None, None


def generate_location_qr(data, output_folder="qr_codes"):
    os.makedirs(output_folder, exist_ok=True)

    # Use safe filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"location_qr_{timestamp}.png"
    file_path = os.path.join(output_folder, file_name)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)

    print("✅ QR Code generated successfully!")
    print("📍 Embedded data:", data)
    print("💾 Saved at:", file_path)


if __name__ == "__main__":
    print("Choose input method:")
    print("1 - Latitude & Longitude")
    print("2 - Google Maps Link")

    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        lat = input("Enter Latitude: ").strip()
        lon = input("Enter Longitude: ").strip()
        maps_url = f"https://www.google.com/maps?q={lat},{lon}"
        generate_location_qr(maps_url)

    elif choice == "2":
        link = input("Paste Google Maps link: ").strip()

        # Try extracting lat/lng (optional)
        lat, lon = extract_lat_lng_from_url(link)

        if lat and lon:
            print(f"📌 Extracted Latitude: {lat}, Longitude: {lon}")

        generate_location_qr(link)

    else:
        print("❌ Invalid choice")