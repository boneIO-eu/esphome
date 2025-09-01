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
json_destination = "../website/public/esp"
firmware_destination = "../website/public/esp/firmware"


def json_pattern(firmware_name):
    return {
        "name": "ESPHome",
        "version": "2025.8.2",
        "home_assistant_domain": "esphome",
        "funding_url": "https://esphome.io/guides/supporters.html",
        "new_install_prompt_erase": False,
        "builds": [
            {
                "chipFamily": "ESP32",
                "parts": [
                    {
                        "path": f"/esp/firmware/{firmware_name}.bin",
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
    filename = get_boneio_name(file)
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

    with open(
        f"{json_destination}/{filename}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(
            json_pattern(firmware_name=filename),
            f,
            ensure_ascii=False,
            indent=4,
        )
