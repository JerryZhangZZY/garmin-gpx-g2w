import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from xml.dom.minidom import parse
import math
import os
import subprocess

# Constants and functions for coordinate transformation
pi = 3.1415926535897932384626  # π
x_pi = pi * 3000 / 180.0
a = 6378245.0  # Semi-major axis
ee = 0.00669342162296594323  # Eccentricity squared


def gcj02_to_wgs84(lng, lat):
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _transform_lat(lng - 105.0, lat - 35.0)
    dlng = _transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def _transform_common(lng, lat, extra_offset):
    ret = extra_offset + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transform_lat(lng, lat):
    return _transform_common(lng, lat, -100.0 + 3.0 * lat)


def _transform_lng(lng, lat):
    return _transform_common(lng, lat, 300.0 + lng)


def out_of_china(lng, lat):
    return not (73.66 < lng < 135.05 and 3.86 < lat < 53.55)


def convert_gpx(input_file):
    output_file = input_file.replace('.gpx', '_wgs84.gpx')

    # Parse GPX file
    dom_tree = parse(input_file)
    gpx_node = dom_tree.documentElement
    trkpt_node = gpx_node.getElementsByTagName("trkpt")

    for trkpt in trkpt_node:
        lon = float(trkpt.getAttribute("lon"))
        lat = float(trkpt.getAttribute("lat"))
        wgs84_coords = gcj02_to_wgs84(lon, lat)
        trkpt.setAttribute("lon", str(wgs84_coords[0]))
        trkpt.setAttribute("lat", str(wgs84_coords[1]))

    with open(output_file, 'w', encoding='utf-8') as f:
        dom_tree.writexml(f, encoding='utf-8')

    return output_file


def upload_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("GPX Files", "*.gpx")])
    if file_paths:
        successful_conversions = []
        failed_conversions = []
        for file_path in file_paths:
            try:
                output_file = convert_gpx(file_path)
                successful_conversions.append(output_file)
            except Exception as e:
                failed_conversions.append((file_path, str(e)))

        if successful_conversions:
            messagebox.showinfo("Success", "Files converted successfully!")
            open_directory(successful_conversions[0])
        if failed_conversions:
            messagebox.showerror("Error", f"Failed to convert the following files:\n" + "\n".join(
                [f"{fp}: {er}" for fp, er in failed_conversions]))


def open_directory(output_file):
    directory = os.path.dirname(output_file)
    if os.name == 'nt':  # Windows
        os.startfile(directory)
    elif os.name == 'posix':  # macOS or Linux
        subprocess.Popen(['open' if sys.platform == 'darwin' else 'xdg-open', directory])


root = tk.Tk()
root.title("Garmin GPX Coordinate Converter")
root.geometry("350x150")
root.resizable(False, False)

frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(frame, text="Convert GCJ-02 to WGS-84 coordinate system", font=("Helvetica", 14))
title_label.pack(pady=10)

upload_btn = ttk.Button(frame, text="Upload GPX Files", command=upload_files)
upload_btn.pack(pady=15)

root.mainloop()
