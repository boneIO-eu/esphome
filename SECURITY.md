# Security Policy

boneIO ESP controllers are DIN-rail relay, cover, dimmer and input modules for
building automation. They ship with ESPHome firmware built from the
configurations in this repository.

This policy says who is responsible for which part of that firmware, how to
report a vulnerability, and what we do with the report.

## Who makes what

**ESPHome is not our software.** ESPHome — the firmware framework, its
components, the native API, OTA, the web server, ESPHome Builder (the
dashboard) and the Home Assistant integration — is developed and maintained by
the ESPHome project under the
[Open Home Foundation](https://www.openhomefoundation.org/). Its design
decisions, its threat model and the fixing of vulnerabilities in it belong to
that project: see the
[ESPHome security policy](https://github.com/esphome/esphome/security)
and [ESPHome security best practices](https://esphome.io/guides/security_best_practices/).

**boneIO** makes the controller hardware and, in this repository:

- the device configurations (`boneio-*.yaml`) and the packages in `packages/`
- the factory firmware we build from them and flash at production, and publish
  for the web installer at <https://boneio.eu/esp>
- the external components we maintain (for example `boneIO-eu/esphome-LM75`)
- the defaults those configurations ship with

So a flaw in how ESPHome itself works — the API protocol, the OTA mechanism,
the web server — is fixed by ESPHome, not by us. A flaw in what *we* chose to
enable, leave open or write ourselves is ours.

### What that means for you

We do not modify ESPHome. A controller you have adopted in ESPHome Builder runs
firmware *you* compile from *your* copy of the configuration, with the ESPHome
version *you* installed. From then on its security depends on that
configuration and on keeping ESPHome up to date — which we cannot do for you.

What we do on our side:

- if you report an ESPHome vulnerability to us, we pass it on to the ESPHome
  project rather than sit on it;
- once ESPHome publishes a fix that affects our controllers, we release new
  factory firmware built on it and say so in the release notes;
- we keep our configurations, packages and defaults free of known
  vulnerabilities, and fix the ones that are ours.

## Reporting a vulnerability

**Please do not open a public issue for a security problem.**

- **ESPHome itself** — report to the ESPHome project, following
  [their policy](https://github.com/esphome/esphome/security). If you are
  not sure whether it is theirs or ours, send it to us; we will route it.
- **boneIO configurations, packages, factory firmware or our components** —
  use GitHub private vulnerability reporting on this repository (**Security** tab
  → *Report a vulnerability*), or email <security@boneio.eu> with `SECURITY` in
  the subject.

You can also report through [CERT Polska](https://cert.pl/cvd/), which
coordinates disclosure with us.

Helpful to include: the controller model and board version, the firmware
release (`esphome-<version>-<build>`) or the ESPHome version you compiled with,
whether the device is factory-flashed or adopted, and the steps to reproduce.

## What we do

| When | What |
|---|---|
| Within 5 working days | We acknowledge the report and tell you who is handling it. |
| Within 10 working days | We tell you whether it is ours or ESPHome's, whether we reproduced it, and roughly when a fix will land. |
| While we work | We keep you updated at least every two weeks. |
| At release | We publish the fix, credit you as you asked, and tell you before it goes public. |

We work to **coordinated disclosure**, with a default embargo of **90 days**
from acknowledgement or until a fix is released, whichever is sooner. We
request a CVE identifier for anything in our part that affects a released
firmware.

If a vulnerability in our part is **actively exploited**, we report it under
the EU Cyber Resilience Act (Regulation (EU) 2024/2847) to ENISA and the
relevant CSIRT.

## Scope

**In scope**

- configurations and packages in this repository
- factory firmware builds and the web installer at <https://boneio.eu/esp>
- external components published by boneIO
- default settings our configurations ship with

**Out of scope**

- ESPHome, ESPHome Builder and the Home Assistant ESPHome integration — report
  those to the ESPHome project
- configurations changed by the owner after adoption
- attacks that need physical access to the controller or its USB port
- third-party components that are not ours

## Factory defaults

Factory firmware is built from public files, so it cannot contain a password or
key unique to your controller. Out of the box the native API is not encrypted,
ESPHome OTA has no password (ESPHome Builder installs your configuration through
it during adoption) and the device web page has no login.

Securing the controller is a step to take right after adoption:
<https://boneio.eu/en/docs/esp/security>.

## Supported versions

| What | Status |
|---|---|
| Latest firmware release for each model (`esphome-<version>-<build>`) | Supported |
| Older firmware releases | Update to the latest |
| Adopted controllers | Supported as configurations: take the current file from this repository and recompile with a current ESPHome |

## How we tell you about fixes

- release notes for each firmware release in this repository
- GitHub Security Advisories, with the CVE where one has been assigned
- <https://boneio.eu/en/docs/esp/security>
