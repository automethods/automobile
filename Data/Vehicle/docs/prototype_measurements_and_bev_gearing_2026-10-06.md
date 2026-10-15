---
doc: Data/Vehicle/docs/prototype_measurements_and_bev_gearing_2026-10-06.md
type: reference
status: active
authority: informative
component: vehicle-data
summary: Reviewed vehicle measurements, remaining gaps, cycle context and manual BEV gearing.
read-first: ["Data/Vehicle/README.md"]
roadmap: []
---

# Vehicle measurements and BEV gearing audit

The 6 October 2026 pass adds 153 reviewed measurements for 36 existing
vehicles: 26 BEVs and 10 PHEVs. It fills 23 previously blank legacy cells
and 16 cells in the new gross/usable battery columns. All 724 prototype
identities and previously populated specification values are preserved.
Generated timestamps and provenance are refreshed by the builder.

The application displays published acceleration, capacity, consumption and
range with their sources. Section 8 also estimates BEV range from verified
usable capacity and the current model's battery-side cycle energy. Section
4 accepts one or two manually declared gearbox ratios multiplied by a
separate final drive; traction and component calculations share this input.

## Coverage

Counts describe positive populated scalar cells across the full catalogue.
Intervals, published maxima and wheel alternatives are available separately
and deliberately do not increase the scalar counts.

| Field | Before | After |
| --- | ---: | ---: |
| Acceleration 0–100 km/h | 365 | 370 |
| Battery capacity with legacy or unspecified basis | 44 | 49 |
| Gross battery capacity | 0 | 9 |
| Usable battery capacity | 0 | 7 |
| Combined energy consumption | 9 | 15 |
| Combined fuel consumption | 226 | 227 |
| Electric or charge-depleting range | 9 | 15 |

The reviewed table contains 40 manufacturer measurements, 13 NEDC, 24 WLTP
and 76 Canadian NRCan measurements. Manufacturer records include capacity
and performance measurements without a driving-cycle claim.

[`../out/prototype_missing_measurements.csv`](../out/prototype_missing_measurements.csv)
lists 59 of the 60 BEV/PHEV rows with remaining review gaps or scalar blanks.
It separates absent reviewed measurements, absent scalar values and unknown
procedures; a scalar blank may be intentional when a published interval is
available. Among the 60 rows, 53 lack reviewed usable capacity, 46 lack
reviewed 0–100 acceleration, 31 lack reviewed combined energy consumption
and 25 lack reviewed electric/charge-depleting range. Eight of 17 PHEVs lack
a reviewed fuel measurement. These are review coverage counts, including
vehicles outside the application's passenger-car scope.

## Sources and configurations

Local literature was checked first. The BMW i3 94 Ah REx specification valid
July 2016 supplies gross/usable capacity and separate 19-inch/20-inch NEDC
ratings for the unchanged pre-facelift variant. The local 2014 UK Outlander
PHEV brochure separates full-charge, weighted and minimum-charge figures;
134 Wh/km is converted to 13.4 kWh/100 km. Local Ampera 0–60 mph data and
later-year approvals were withheld from the 2012 record.

Local NRCan BEV and PHEV CSVs were matched by model year and drivetrain,
with reviewed spelling aliases. Their Canadian ratings retain market `CA`
and procedure `NRCan`; they are not relabelled WLTP or EPA. Tesla Plaid
19/21-inch and 20/22-inch wheel configurations remain separate. C-MAX
Energi charge-depleting range is identified as such because that mode can
also consume gasoline.

Primary manufacturer sources cover the original BMW i3, Audi Sportback 50,
Honda e, Mazda MX-30, BMW iX xDrive40, F56 Mini Cooper SE, original Taycan 4S,
BYD ATTO 3, SF90 Stradale, facelift BMW 530e, Mazda R-EV and Dolphin Active.
Every value has its own URL/file and locator in
[`../sources/prototype_measurements.csv`](../sources/prototype_measurements.csv).
For example, the [2024 Dolphin European table](https://www.byd.com/content/dam/byd-site/eu/pdfs/dolphin/Dolphin-0724-BPS-EN-V7-web.pdf)
identifies the Active column, and Mazda's [June 2023 release](https://nl.mazda-press.com/news/2023/mazda-start-de-massaproductie-van-de-mx-30-e-skyactiv-r-ev/)
identifies the R-EV combined WLTP values. Later-generation Mini and updated
2021 Taycan specifications were withheld from earlier vehicle rows.

## Existing disagreements

Reviewed alternatives are displayed with their evidence. Existing scalar
values are preserved, so consumers using only the old CSV columns still
need to resolve these conflicts:

| Vehicle | Existing scalar | Reviewed source |
| --- | --- | --- |
| Honda e Advance 2020 | 0–100: 9.5 s | Advance: 8.3 s |
| BYD ATTO 3 2023 | Battery: 62 kWh | 60.48 kWh, gross/net unspecified |
| Tesla Model S Plaid 2022 | Combined: 17.5 kWh/100 km; range: 652 km | NRCan 19-inch: 18.1 and 637; 21-inch: 20.8 and 560. Existing values match regular Model S. |
| BMW 530e 2020 facelift RWD | Combined fuel: 17 L/100 km | WLTP weighted interval: 1.3–1.9 L/100 km |
| BMW i3 60 Ah REx 2015 | Combined fuel: 6 L/100 km | Original specification: 0.6 L/100 km NEDC weighted |

## WLTC range and measurement basis

The application supports complete JRC traces for WLTC 3a and 3b. The legacy
preset ID `wltc3` denotes Class 3b; `wltc3a` denotes Class 3a. Imported custom
traces receive no inferred class. Published WLTP does not establish a
subclass: none of the reviewed manufacturer/rating sources explicitly names
3a or 3b, so those published class cells remain blank.

For a BEV with one consistent reviewed usable-capacity value and a positive,
valid, speed-compatible model integral, estimated range is
`100 × usable battery kWh / battery-side kWh per 100 km`. The application
does not substitute gross/unspecified capacity, calculate PHEV range from
weighted energy, or present this model estimate as certified WLTP. Plug-side
published consumption and battery-side model consumption remain separate.
The estimate uses the current project inputs and a full usable charge;
temperature effects and battery ageing are outside this model.

## Manual BEV gearing

Choose the gearbox-row/final-drive mode in section 4, select the driven axle,
enter one or two positive descending gear ratios and the final ratio, then
select the active gear. For example, gears `2; 1` with final drive `4` give
motor-to-wheel reductions `8; 4`. The active gear determines traction and
motor speed throughout the cycle; automatic shifting is not modelled.

Separate component calculations divide the final ratio out of the total
exactly once. Gearbox maximum-torque and maximum-speed checks use the full
declared gear set. Half-shaft torque includes the final drive, and a separate
final-drive design receives the gearbox-output torque. The new mode covers
one driven axle without an additional wheel-end reduction.

Full-reduction mode retains per-axle totals and supports a two-speed axle
alongside a single-speed axle, including the Taycan rear `16; 8.05` and front
`8.05`. An old catalog can list its top-speed reduction first; that order is
preserved. Old saved projects default to full-reduction mode and the first
declared ratio. Manual gear/final values are ignored in full-reduction mode;
stored axle totals are ignored in gearbox-row/final-drive mode.

## Verification

The data build validates identities, units, finite intervals, required source
context and usable capacity no greater than gross capacity. Snapshot
comparison confirms no previously populated specification value changed.
Focused integration tests verify gear multiplication, component loads and
new/old project restoration. Browser checks cover published intervals,
WLTC 3a/3b range, both Taycan rear ratios and manual gearing.
