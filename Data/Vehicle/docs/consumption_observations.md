---
doc: Data/Vehicle/docs/consumption_observations.md
type: spec
status: active
authority: normative
component: data
summary: Source-preserving intake of regulatory, independent, owner and local consumption observations for later calibration.
read-first: ["Data/Vehicle/docs/vehicle_prototypes_design.md", "Data/Vehicle/docs/cycle_consumption_sources.md"]
roadmap: ["R-23", "R-24"]
---

# Referenced consumption observations

Automobile **v0.4.36**, intake contract **1**, 2026-10-07.
The sidecar `Data/Vehicle/sources/prototype_measurements.csv` has **1,413**
observations, including the original 153 unchanged reviewed records and **1,260**
additions. **1,335** records describe fuel/electric consumption, covering **72**
prototype identities. The 724-row principal catalogue is unchanged.

The intake checks local files first: NRCan city/highway/combined rating files;
the Argonne 2016 Volt test-summary PDFs inside `Vehicle_simulation/Test_PHEV_Data`;
and Outlander trip metrics from `Vehicle_simulation/My_PHEV`, derived from
`Drive_cycles_prjct` OBD logs. Online additions use the official EPA download,
ADAC's Zoe test, a Zoe owner's test and a Leaf owner's original forum post.
Local literature/model handbooks describe equations and assumptions; their
example/simulated values are not promoted to measured consumption.

Every record retains file/URL, page/row/post locator and evidence. New fields
record observation ID, source type, measurement method, rating basis, original
vehicle configuration, match status, conditions JSON, original value/unit,
conversion, calibration status, retrieval date and intake identity. Original
columns and values remain available for existing consumers.

Separate source observations may disagree. They remain separate; no average
or source priority overwrites an adopted design value. A same-source duplicate
with the same locator, conditions and context is refused. The current intake
never fills principal catalogue cells automatically. Explicit future adoption
requires review of configuration, procedure, meter and operating mode.

## Procedure and metering

City, rural, highway, motorway, mixed and constant-speed metrics are supported.
Only phases actually supplied by sources are populated; no rural/highway
equivalence or WLTC phase correspondence is invented. Published WLTP alone
never establishes WLTC subclass 3a/3b.

EPA label-adjusted fuel values and unadjusted laboratory `UCity`/`UHighway`
stay separate. EV MPGe is not liquid fuel consumption. Electricity fields
`cityE`/`highwayE`/`combE` retain original kWh/100 miles, converted to
kWh/100 km using 1.609344 km/mile. PHEV charge-sustaining fuel stays separate
from charge-depleting electricity and weighted manufacturer figures.
[EPA field definitions](https://www.fueleconomy.gov/feg/ws/index.shtml).
EPA electric ratings include AC charging losses and use the outlet metering
basis. [EPA measurement procedure](https://www.epa.gov/greenvehicles/fuel-economy-and-ev-range-testing).

NRCan 2-cycle, 5-cycle and 5-cycle-adjusted series retain their identity and
source row, including separate transmission variants. Known engine size,
diesel/gasoline, drive and transmission conflicts are rejected. Compatible
model/year matches without a proven trim are marked for further review.
[NRCan source dataset](https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64).

The local Argonne archive provides **67** independent observations at nominal
20, 72 and 95 °F. Retain individual test IDs, repetitions, actual cell
temperature, test mass, cold/hot start and HVAC. Battery observations are
power-analyzer DC net energy; CS fuel is emissions-bag fuel economy. `CS` in
the start column means cold start and is distinct from charge-sustaining mode.
Six negative net-battery-energy phases are not exported as positive consumption.
Required source attribution: Downloadable Dynamometer Database, Advanced
Powertrain Research Facility, Argonne National Laboratory, US Department of Energy.
Original archive members and page/row locators are retained; PDFs are not copied
into the app. The local `references` file points to the
[Argonne testing page](https://www.anl.gov/taps/plugin-hybrid-electric-vehicle-testing).

ADAC's Zoe figure includes AC charging losses and is plug-side energy. The
tested 2019–2020 Intens configuration is related evidence for the 2022 prototype,
not an exact year/trim match. The separate owner test records a dashboard value,
tailwind, leg distance and average speed; its metering basis remains unspecified.
[ADAC test](https://www.adac.de/rund-ums-fahrzeug/autokatalog/marken-modelle/renault/renault-zoe/),
[owner test](https://www.elektroauto-zoe.de/test-zoe-r135-ze50-mit-ccs/).
The Leaf owner's 9 km/kWh report retains the original reciprocal unit and
vehicle/battery description; missing conditions remain unspecified.
[Original forum post](https://www.reddit.com/r/leaf/comments/13h6n7r/average_kmor_miles_per_kwh/).

## Local driving observations

The Outlander snapshot retains **763** original trip-summary rows, of which
**752** have finite consumption and positive distance. Eleven stationary rows
have no valid denominator; the audit records their exclusion. Fuel is the
logger's `Fuel Rate` integral, with the original density/temperature derivation.
This is an OBD-derived estimate, not a tank fill or independent fuel instrument.
Predicted fuel, wheel energy, emissions proxies and simulated cycle results are
excluded from this intake of observed consumption.

Each local row refers to the original `trip_fuel_toxicity_metrics.csv` row and
trip filename. The snapshot and intake manifest preserve the origin file hash,
input paths and derivation reference. Battery SOC/energy balance, exact trim,
payload and wheel configuration are not established. These trip values are
excluded from fitting a charge-neutral vehicle model until that context is added.
The app shows the local collection as one range/count row; every individual
observation remains in the CSV, application dataset and SI exchange export.

## Rebuild and exchange

```sh
npm run data:consumption
npm run test:data
```

The offline rebuild uses frozen EPA/Outlander snapshots and reviewed
`consumption_intake.json`, plus existing local NRCan files. It performs no
network requests and is repeatable. The CSV is validated before replacement.
`out/consumption_intake_audit.json` records input hashes and counts;
`out/consumption_coverage.csv` records every prototype's reviewed coverage,
legacy consumption cells and remaining context gaps.

`out/consumption_observations.json` follows the common SI exchange contract:
fuel volume per distance m³/m and electric energy per distance J/m.
Original units, values, conversion and all source context remain attached.
The public schemas, quantity registry and module origins are under
`My_books/vehickle_math_models/contracts`; the project-wide contract is
`My_books/TECHNICAL-MODULES.md`. Future modules belong in that library.

Automobile v0.4.37 adds a separate provisional calibration dataset and report
for the local Argonne Volt archive. The 1,413 observation records retain their
original fields and `needs-context`/`excluded` statuses; the tested-vehicle
cohort does not promote the compatible prototype match to an exact trim.
See [calibration evidence and limits](../../../docs/CONSUMPTION-CALIBRATION.md).
