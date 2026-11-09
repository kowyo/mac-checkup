# mac-checkup

A single-file command-line tool that checks three things on any Mac:

1. **Are the parts original?** It reads the same repair record that System Settings › General › About › Parts & Service uses, and adds indirect checks for the battery, storage, keyboard, display and Touch ID.
2. **Is it locked or managed by someone else?** It checks Activation Lock, MDM and Automated Device Enrollment, MDM bypasses in `/etc/hosts`, configuration profiles, Apple Account sign-in, FileVault and System Integrity Protection.
3. **Can Apple Intelligence be turned on?** It reads macOS's own eligibility verdict and shows which requirement fails: device region, current location, billing country, system and Siri language, and more.

No dependencies, no `sudo`. It only uses tools that ship with macOS.

## Run

```sh
curl -fsSL https://raw.githubusercontent.com/kowyo/mac-checkup/main/mac-checkup | zsh
```

Or install it with [uv](https://docs.astral.sh/uv/):

```sh
uv tool install git+https://github.com/kowyo/mac-checkup
mac-checkup
```

Or download the script:

```sh
mkdir -p ~/.local/bin
curl -fsSL https://raw.githubusercontent.com/kowyo/mac-checkup/main/mac-checkup -o ~/.local/bin/mac-checkup
chmod +x ~/.local/bin/mac-checkup
mac-checkup
```

Options:

| Option | Effect |
|---|---|
| `--show-serial` | Print the full serial number. It is masked by default so you can share the output. |
| `--no-open` | Don't open System Settings to refresh the repair record. |
| `--lang en\|zh` | Output language. Defaults to the system language. |

## Example

```text
Apple repair record (Parts & Service)
  ✓ Display: no repair record, original
  ✓ Lid angle sensor: no repair record, original
  ✓ Logic board: no repair record, original
  ✓ Touch ID: no repair record, original

Locks and management
  ✓ Activation Lock: off
  ✓ Device management (MDM): not enrolled
  ✓ FileVault: on
  ✓ System Integrity Protection: on

Apple Intelligence
  ✗ System verdict: not eligible (eligibilityd)
  ✗ Device region: China mainland (CH/A): Apple Intelligence doesn't currently work on Macs bought in China mainland
  ✓ Apple Account billing country: Singapore
  ✗ System and Siri language match: en-US vs Siri zh-HK; set both to the same language
```

## How it works

| Check | Source |
|---|---|
| Repair record | macOS writes the result of its repair check (`repairHistoryForUI`) to the unified log under `com.apple.corerepair` whenever the About pane loads. The tool reads the latest entry from the last 30 days. If there is none, it opens the About pane in the background, waits for the entry, and closes System Settings again if it wasn't already open. Needs Apple silicon and macOS 26 or later. |
| Region sold in | `region-info` in the I/O Registry, the suffix of the model number (`CH/A`, `LL/A`, …). |
| Battery, storage, keyboard, display | `system_profiler` |
| Touch ID | `bioutil -rs` |
| Activation Lock | `system_profiler SPHardwareDataType` |
| MDM | `profiles status -type enrollment`, plus `/etc/hosts` entries that block Apple's enrollment servers. |
| Configuration profiles | `system_profiler SPConfigurationProfileDataType` |
| FileVault, SIP | `fdesetup status`, `csrutil status` |
| Apple Intelligence | The `GREYMATTER` domain in `/private/var/db/eligibilityd/eligibility.plist`, the verdict System Settings itself relies on (`4` means eligible). Each input is shown as passing or failing. On a macOS without that file, the tool falls back to Apple's published rules. |
| Apple Account region | The App Store storefront ID in `com.apple.itunesstored`. |
| Siri language | `com.apple.assistant.backedup` |

Rules for Apple Intelligence follow Apple's [How to get Apple Intelligence](https://support.apple.com/121115) page, and the repair record follows [About Mac parts and service history](https://support.apple.com/123123).

## Limits

- macOS only tracks a few parts in the repair record: the logic board and Touch ID on every supported Mac, and on newer laptops the display and the lid angle sensor. Batteries, keyboards and most displays have no "genuine" label, so those checks are indirect.
- The repair record and the Apple Intelligence verdict come from data Apple doesn't document, so a future macOS can change them.
- Activation Lock and MDM are read from this Mac. A Mac assigned to an organization in Apple Business Manager can still enroll after it's erased; ask the seller for proof of purchase.
- The firmware password on Intel Macs needs `sudo` to read, so it isn't checked.
- For a definitive answer, ask an Apple Store or Apple Authorized Service Provider to look up the serial number.

## License

MIT
