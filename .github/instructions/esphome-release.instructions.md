---
description: "Use when updating ESPHome versions, firmware GitHub Actions, release tags, validation flows, or package refs in the esphome repository. Covers how to bump to a new ESPHome release, validate configs, and prepare a release tag."
---
# ESPHome Release Update Workflow

- Keep one target ESPHome version across all release-related files. At minimum update `.github/workflows/build-firmware.yml`, `.github/workflows/validate-firmware.yml`, and `create_firmware.py`.
- Never leave the build workflow on `version: latest`. Resolve the version once and pass the exact version into every build step.
- Before editing YAML packages, validate all top-level `boneio-*.yaml` configs against the target image with Docker:
  `docker run --rm -v "$PWD":/config ghcr.io/esphome/esphome:<version> config <file>`
- Treat successful validation of all top-level configs as the release gate for ESPHome bumps.
- Preserve the existing release tag format: `esphome-<esphome_version>-<build>`, for example `esphome-2026.4.0-b1`.
- Keep GitHub Release notes explicit: mention the pinned ESPHome version, firmware bundle version, and the GitHub Pages catalog URL.
- Do not modify generated `.esphome/` outputs as part of the version bump unless the task explicitly asks for committed build artifacts.
- If a config fails on the new ESPHome version, fix the root YAML or shared package in `packages/` instead of weakening validation.