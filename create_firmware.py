#!/usr/bin/python
import glob
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

home = str(Path.home())


cwd = os.getcwd()


pattern = r"name:\s*(\S+)"
json_destination = "../website2/public/fwesp"
firmware_destination = "../website2/public/fwesp/firmware"
firmware_destination2 = "../esphome_uploader/firmware"


def json_pattern(firmware_name, chip_family="ESP32"):
    return {
        "name": "ESPHome",
        "version": "2025.8.2",
        "home_assistant_domain": "esphome",
        "funding_url": "https://esphome.io/guides/supporters.html",
        "new_install_prompt_erase": False,
        "builds": [
            {
                "chipFamily": chip_family,
                "parts": [
                    {
                        "path": f"/fwesp/firmware/{firmware_name}.bin",
                        "offset": 0,
                    }
                ],
            }
        ],
    }


def get_boneio_name(file):
    with open(file) as f:
        next(f)
        name = next(f)
        match = re.search(pattern, name)
        if match:
            extracted_text = match.group(1)
            return extracted_text
        return None


for file in glob.glob("*.yaml"):
# for file in glob.glob("boneio-dimmer_gen2_8ch-v0_1.yaml"):
    filename = get_boneio_name(file)
    chip_family = "ESP32-S3" if "gen2" in filename else "ESP32"
    if not filename:
        print("No file found.")
        break
    firmware_path = f"{cwd}/.esphome/build/{filename}/.pioenvs/{filename}/firmware.factory.bin"
    cmd = f'docker run --rm -p 6052:6052 -v "{cwd}":/config -it ghcr.io/esphome/esphome compile {file}'
    print(cmd)
    result = subprocess.run(
        cmd,
        shell=True,
    )
    if result.returncode != 0:
        print("Process failed, breaking.")
        break
    shutil.copyfile(firmware_path, f"{firmware_destination}/{filename}.bin")
    shutil.copyfile(firmware_path, f"{firmware_destination2}/{filename}.bin")

    with open(
        f"{json_destination}/{filename}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(
            json_pattern(firmware_name=filename, chip_family=chip_family),
            f,
            ensure_ascii=False,
            indent=4,
        )
