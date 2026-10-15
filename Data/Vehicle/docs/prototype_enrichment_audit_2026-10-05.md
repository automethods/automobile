---
doc: Data/Vehicle/docs/prototype_enrichment_audit_2026-10-05.md
type: reference
status: active
authority: informative
component: vehicle-data
summary: Local-first prototype enrichment, coverage, field evidence and unresolved source identities.
read-first: ["Data/Vehicle/README.md"]
roadmap: []
---

# Prototype specification audit — 5 October 2026

The catalogue grew from 718 to 724 vehicles. Reviewed specifications filled
1,500 previously blank cells on existing vehicles. Existing derivation rules
also populated 177 driven-axle counts and 18 specific-power values: 1,695 filled
cells in total, across 348 existing vehicles. No previously populated
specification value changed. All 718 original prototype IDs remain present.

The six additions are Australian MY26 Nissan Navara SL, ST, ST-X and PRO-4X
dual-cab automatic pickups, and Y62 Patrol Ti and Ti-L. They have separately
identified trims, masses, dimensions, tyres, engine ratings, gearbox/final-drive
and high/low transfer ratios, seating, towing limits and fuel consumption.

## Coverage

Counts below describe populated cells, not independently certified vehicles.
The new column includes the six added vehicles. A blank may be unresolved or
inapplicable: electric vehicles do not require combustion-engine displacement,
and most road cars have no two-range transfer case.

| Field | Before, 718 vehicles | After, 724 vehicles | Remaining blank |
| --- | ---: | ---: | ---: |
| Tyre designation | 180 | 371 | 353 |
| Length | 444 | 626 | 98 |
| Body width | 435 | 616 | 108 |
| Height | 437 | 618 | 106 |
| Wheelbase | 693 | 701 | 23 |
| Track width | 223 | 382 | 342 |
| Drive layout | 269 | 452 | 272 |
| Powertrain | 598 | 717 | 7 |
| Engine displacement | 437 | 617 | 107 |
| Rated power | 492 | 516 | 208 |
| Braked towing limit | 12 | 40 | 684 |
| Battery capacity | 41 | 44 | 680 |
| Static wheel radius | 1 | 1 | 723 |
| Dynamic wheel radius | 77 | 77 | 647 |

The remaining basic specification gaps are listed for 480 in-scope vehicles in
[`../out/prototype_missing_reference_fields.csv`](../out/prototype_missing_reference_fields.csv).
This list covers tyres, dimensions, track width, drive layout, powertrain and
power (accepting an existing motor-power value for an electric vehicle).
It does not treat every blank engineering coefficient as a required field.
The gap list is a snapshot of this audit, rather than an automatically rebuilt
source table.

## Local evidence used first

The requested `Transport/My_books` folder and the neighbouring original
literature collection were reviewed. Books stay outside the application;
the field evidence retains their filenames and page locators.

| Source | Location | Use |
| --- | --- | --- |
| Bosch automotive handbook, Russian second edition | `/media/cigameca/SHARED/Work/Literature/Transport/Automobiles/Spravochnik/1Авто справочник Bosch 2е рус издание.pdf` | Printed pp. 934–965; PDF pages 915–946; property 34. Visually checked headings and tyre cells supplied 158 missing tyre designations. |
| Car Specification Dataset 1945–2020 | `Data/Data sources/Car Specification Dataset 1945-2020/Car Dataset 1945-2020.csv.zip` | 1,149 direct field candidates and 152 mean-track calculations from the source rows used by the existing import or an unambiguous identity match. Original [dataset citation](https://doi.org/10.34740/kaggle/ds/2938279). |
| Nissan Navara MY26 manufacturer table | `/media/cigameca/SHARED/Work/Literature/Transport/Automobiles/by brands/All-new MY26 Navara Spec Sheet AUS.pdf` | PDF pp. 1–2; four distinct Australian trim columns. |
| Nissan Patrol MY26 manufacturer table | `/media/cigameca/SHARED/Work/Literature/Transport/Automobiles/by brands/MY26 Patrol Spec Sheet AUS.pdf` | PDF pp. 1–2; March 2026; Ti and Ti-L columns. |
| Opel Ampera brochure | `/media/cigameca/SHARED/Work/Literature/Transport/Automobiles/by brands/EV_hybrid/REEV/Ampera_Spec_PG_17_December_2013.pdf` | Corroborates the tyre marking from the year-matched 2012 online brochure. |

Bulk values retain the `bulk_dataset` method; they are not manufacturer
verification. Existing Kaggle expansion rows were matched back to their
original first selected record, checking generation and both masses.
Other rows required a unique make/model/year/trim match. Seven proposed
matches were withheld for identity/mass mismatches or implausible payloads:
`vp-b8a9e9`, `vp-19cbda`, `vp-2a9557`, `vp-4c07e7`, `vp-f6459c`,
`vp-d32702`, `vp-e348be`. The source labels a 1989 Chevrolet Kadett Flexfuel
as “Hybrid”; that label was withheld because it does not establish a hybrid
electric powertrain.

## Internet evidence for remaining gaps

Online sources were checked on 5 October 2026. Each value has a separate
identity-bound entry in `sources/prototype_specifications.csv`.

- Tesla [2017–2023 Model 3 manual](https://www.tesla.com/ownersmanual/2017_2023_model3/en_us/GUID-FDDB10EF-FFA9-46EB-B8CC-03614AE92B6B.html)
  and [2020–2024 Model Y manual](https://www.tesla.com/ownersmanual/2020_2024_modely/en_us/GUID-FDDB10EF-FFA9-46EB-B8CC-03614AE92B6B.html):
  tyre configurations for eight existing rows. Available wheel options are
  labelled; the catalogue does not establish which option was originally
  fitted. The later Model 3 staggered rear tyre was excluded.
- Audi [first-generation e-tron aerodynamics press information](https://uploads.audi-mediacenter.com/system/production/uploaded_files/13466/file/d52c434bebeb3571de14cac7c11ec89c296122cf/en_Press_Information_Audi_e-tron_Aerodynamics.pdf?1544010563=&disposition=attachment):
  geometry and the standard 19-inch tyre configuration for the 2021 e-tron
  55 quattro row; PDF pp. 2 and 5.
- BMW [March 2015 i3 specification](https://www.press.bmwgroup.com/south-africa/article/attachment/T0206382EN/299097):
  the 60-Ah REx standard 19-inch front/rear configuration, PDF p. 3. The
  manufacturer table is South African; the shared I01 wheel configuration
  is identified in the evidence, rather than presented as an EU approval.
- Vauxhall [October 2012 Ampera specification](https://business.citroen.be/content/dam/vauxhall/Home/PDFs/historical-brochures/discounted-models/ampera/Ampera_Spec_PG_2_October_2012.pdf):
  standard tyre configuration, PDF p. 9.
- Mazda [January 2023 technical brochure](https://media-assets.mazda.eu/raw/upload/mazdabe/globalassets/pdfs/brochure/mx30-r-ev_r-edition_flyer_jan2023_nl_web.pdf?rnd=48e61e),
  [launch release](https://newsroom.mazda.com/en/publicity/release/2023/202301/230113a.html)
  and [European R-EV technology page](https://pt.mazda-press.com/tecnologia/motores/e-skyactiv-r-ev/):
  tyre, battery, rotary displacement, motor ratings, performance and WLTP
  values. The brochure's pre-homologation caveat is retained in field evidence.
  Width and height were withheld because contemporary brochures disagree;
  folded-mirror width must not become body width. PHEV weighted fuel use is
  distinct from consumption with the battery depleted.
- Porsche [2019 Taycan 4S launch](https://newsroom.porsche.com/en_AU/2019/products/porsche-taycan-4s-electric-sports-car-entry-level-model-18901.html)
  and [AfterSales certificate 58/22 ENU 4400](https://www.taycanforum.com/forum/attachments/tsb-wheel-size-and-pressures-jan-2023-pdf.73516/):
  battery capacity, performance, AWD and the 19-inch front/rear tyre
  configuration for the two 2020 rows. The certificate is Porsche-authored
  and hosted on TaycanForum. Later facelift specifications and launch-control
  overboost power were excluded from the rated-power field.
- Hyundai Motor America [2024 Santa Fe equipment matrix](https://device.report/m/cdf2713c9f59ce86dcdc1d30a323582319f7958abce9ef8f18dab3373ca563fc.pdf):
  the US SE tyre configuration, PDF p. 1. Manufacturer-authored PDF hosted
  on device.report; other markets and trim options were not substituted.

## Withheld data and existing import issues

These findings concern existing rows and are not silently corrected by this
gap-filling pass.

- Bosch printed p. 955 / PDF page 936 has seven vehicle columns in this order:
  Fiat Ulysse, Lamborghini Diablo, Lancia Y, Delta, Dedra, Kappa, Z. The existing
  parser starts with Lamborghini and puts Fiat last, shifting specifications
  against vehicle labels. New tyre values were withheld for `vp-51cbf9`,
  `vp-94c564`, `vp-165679`, `vp-693059`, `vp-3e4ee2`, `vp-a15973`, `vp-f6199c`.
  Existing specifications on these seven rows need a separate complete
  re-extraction against the correct column headings.
- Bosch printed p. 938 labels the Focus as 1.8, while the current row
  `vp-72edb9` says 1.6; printed p. 945 labels the Xsara as 1.8, while
  `vp-0d9c43` says 1.6i. Tyres were withheld for both unresolved identities.
- BMW Z3 3.2 (`vp-688080`) and Smart 0.8 TD (`vp-9751a6`) have incomplete
  tyre footnotes in the available Bosch scan; no missing component was guessed.
- Several EV_sim rows already store dynamic radii such as 0.2413 m or
  0.2667 m, equal to 19/21-inch rim radii. These are questionable rolling
  radii and were preserved for separate source review. Added tyre markings
  do not validate those radii.
- Some local brochures specify only a rim diameter, tyre alternatives,
  mass ranges or an incomplete trim identity. Those gaps remain unresolved.
  Historic tyre markings without an aspect ratio retain the omission;
  no static/rolling radius, deflection factor, Cd or drivetrain efficiency
  was invented. Different front/rear tyres remain explicit in the text;
  a calculation using one representative tyre still needs an axle choice.

## Rebuild and checks

Edit the sparse enrichment overlay for new vehicles and the field-evidence
CSV for gap filling. Rebuild in this order:

```sh
python3 -B Data/Vehicle/build/build_vehicle_prototypes.py
python3 -B Data/Vehicle/build/build_prototype_dataset.py
python3 -B Data/Vehicle/build/build_q_dataset.py
python3 -B Data/Vehicle/build/build_chapter4_dataset.py
python3 -B -m unittest discover -s Data/Vehicle/build -p 'test_*.py'
npm test
```

The browser data contains 694 in-scope prototypes, 521 q points, and 435
tyre/radius suggestions. Thirty motorcycles remain explicitly excluded.
Manufacturer page evidence for the six new Nissan rows also lives in
`reference_geometry_sources.json`, preserving trim-specific dimensions
when the general same-model disagreement check flags those differences.

The field importer has focused tests for identity, citation completeness,
finite numeric values, duplicate fields, preservation of known values and
source disagreements. The historic WR/SR tyre forms from the local handbook
are also accepted by the tyre parser.

Validation passed: 194 Python data tests, 67 focused JavaScript tests, the
documentation checker, unique-ID and baseline-preservation checks, and the
six new vehicles' geometry propagation into the selector.

The broader `npm test` run reported an existing source-text assertion failure
in `characteristic-integration.test.js:210`: it expects
`VehicleReportCalculationData.notesFor(step)` in `report.js`. Neither file was
changed by this audit. That standalone file reproduced the failure (25 of 26
tests passed). The broader run subsequently stopped producing output during
the script tests and was interrupted; a full-suite pass is not claimed.
