"""Validate referenced operation observations and emit deterministic exchange data."""
import csv
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERSION = '0.1.2'
UNITS = {
    'vehicle_price': 'currency/bus', 'procurement_package_price': 'currency/lot',
    'service_cost': 'currency/service', 'maintenance_cost_per_distance': 'currency/mi',
    'tyre_cost_per_distance': 'currency/mi', 'tyre_replacement_exposure': 'mi/event',
    'tyre_replacement_count': 'event', 'tyre_replacement_labour': 'h',
    'oil_filter_interval': 'km', 'fuel_filter_interval': 'km', 'coolant_interval': 'km',
    'valve_adjustment_interval': 'km', 'dpf_cleaning_interval': 'km', 'def_filter_interval': 'km',
    'service_interval': 'km', 'service_to1_interval': 'km', 'service_to2_interval': 'km',
    'daily_inspection_interval': 'working-day', 'seasonal_service_frequency': 'event/year',
    'passenger_capacity': 'person', 'optional_folding_seats': 'person', 'passenger_doors': 'door',
    'charging_power': 'kW', 'charging_time': 'h', 'battery_capacity': 'kWh',
    'battery_warranty_years': 'year', 'battery_warranty_soh': '%',
    'warranty_distance': 'km', 'warranty_months': 'month', 'availability': '%',
    'bus_roadcalls': 'event', 'propulsion_roadcalls': 'event', 'low_voltage_battery_changeouts': 'event',
    'failure_case': 'case', 'range_claim': 'km', 'geometry_candidate_length': 'mm',
    'geometry_candidate_width': 'mm', 'geometry_candidate_height': 'mm', 'geometry_candidate_wheelbase': 'mm',
    'geometry_candidate_track_front': 'mm', 'geometry_candidate_track_rear': 'mm',
    'engine_power_unclassified_hp': 'hp-unspecified',
}
# Calendar months/years and money retain their basis; no fixed-day or FX conversion.
SI = {'km': ('m', 1000), 'mm': ('m', .001), 'h': ('s', 3600),
      'kW': ('W', 1000), 'kWh': ('J', 3600000), '%': ('1', .01),
      'mi/event': ('m/event', 1609.344)}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def number(value):
    if value in ('', None):
        return None
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ValueError('Nonfinite or negative observation')
    return result


def validate_row(row, prototypes, sources):
    if not all(row.get(k, '').strip() for k in ['id', 'scope_kind', 'scope_id', 'metric', 'unit', 'source_id', 'locator', 'notes']):
        raise ValueError('Missing observation identity, evidence or scope')
    if row['metric'] not in UNITS or row['unit'] != UNITS[row['metric']]:
        raise ValueError('Unknown metric/unit')
    if row['scope_kind'] not in {'prototype', 'class', 'component', 'fleet', 'procurement', 'infrastructure'}:
        raise ValueError('Invalid subject scope')
    if row['source_id'] not in sources:
        raise ValueError('Unknown source')
    pid = row.get('prototype_id', '')
    if pid and pid not in prototypes:
        raise ValueError('Unknown prototype')
    if row['scope_kind'] == 'prototype' and (not pid or row['scope_id'] != pid):
        raise ValueError('Prototype subject mismatch')
    if row['match_status'] not in {'exact-source-variant', 'compatible-configuration', 'related-variant', 'not-prototype-specific'}:
        raise ValueError('Invalid prototype match status')
    if not pid and row['match_status'] != 'not-prototype-specific':
        raise ValueError('Missing prototype for match assertion')
    if row['match_status'] == 'exact-source-variant' and row['scope_kind'] != 'prototype':
        raise ValueError('A fleet/class record is not an exact prototype observation')
    lo, hi = number(row.get('value_min')), number(row.get('value_max'))
    statistic = row['statistic']
    if statistic not in {'exact', 'interval', 'minimum', 'maximum', 'approximate', 'narrative'}:
        raise ValueError('Invalid statistic')
    if statistic == 'narrative':
        if row['metric'] != 'failure_case' or lo is not None or hi is not None:
            raise ValueError('Narrative cases have no invented frequency')
    elif statistic == 'minimum':
        if lo is None or hi is not None:
            raise ValueError('Lower bound must have an unknown upper bound')
    elif statistic == 'maximum':
        if hi is None or lo is not None:
            raise ValueError('Upper bound must have an unknown lower bound')
    elif lo is None or hi is None or lo > hi or (statistic in {'exact', 'approximate'} and lo != hi):
        raise ValueError('Invalid observation interval')
    context = json.loads(row.get('context_json') or '{}')
    if not isinstance(context, dict):
        raise ValueError('Context must be an object')
    json.dumps(context, allow_nan=False)
    currency = row.get('currency') or None
    if row['unit'].startswith('currency/'):
        if currency not in {'UAH', 'USD', 'EUR', 'GBP', 'SEK'} or not all(k in context for k in ['priceBasis', 'taxBasis']):
            raise ValueError('Money needs currency, price and tax basis')
    elif currency:
        raise ValueError('Currency on a nonmonetary value')
    for key in ['distanceKm', 'engineHours', 'calendarMonths']:
        if key in context and (number(context[key]) is None or number(context[key]) <= 0):
            raise ValueError('Invalid service deadline')
    if 'calendarMonths' in context or 'engineHours' in context:
        if context.get('triggerRule') != 'first-reached':
            raise ValueError('Combined deadlines require first-reached semantics')
    if row['metric'] in {'tyre_replacement_exposure', 'bus_roadcalls', 'propulsion_roadcalls', 'low_voltage_battery_changeouts', 'tyre_replacement_count'}:
        if row['scope_kind'] != 'fleet' or number(context.get('fleetVehicles')) in (None, 0) or number(context.get('fleetDistanceMi')) in (None, 0):
            raise ValueError('Fleet wear/failures need sample and exposure; no implied service life')
    source = sources[row['source_id']]
    scale = SI.get(row['unit'])
    return dict(schema='technical-vehicle-operation-observation/1', id=row['id'],
                subject=dict(kind=row['scope_kind'], id=row['scope_id'], prototypeId=pid or None, matchStatus=row['match_status']),
                metric=row['metric'], value=dict(min=lo, max=hi, unit=row['unit'], statistic=statistic, currency=currency),
                canonical=dict(min=lo * scale[1] if lo is not None else None,
                               max=hi * scale[1] if hi is not None else None, unit=scale[0]) if scale else None,
                market=row['market'], asOf=row.get('as_of') or None, context=context,
                sourceId=row['source_id'], sourceFile='Data/Vehicle/operations/' + source['artifact'],
                sourceUrl=source.get('url'), sourceSha256=source['artifactSha256'],
                locator=row['locator'], notes=row['notes'], adoption='explicit-scenario-only')


def build(root=HERE):
    root = Path(root)
    sources_document = json.loads((root / 'sources.json').read_text())
    sources = {s['id']: s for s in sources_document['sources']}
    if len(sources) != len(sources_document['sources']):
        raise ValueError('Duplicate source IDs')
    for source in sources.values():
        artifact = Path(source['artifact'])
        if artifact.is_absolute() or '..' in artifact.parts or sha(root / artifact) != source['artifactSha256']:
            raise ValueError('Source path or hash mismatch')
    with (root.parent / 'vehicle_prototypes.csv').open(newline='', encoding='utf-8-sig') as stream:
        prototypes = {r['prototype_id']: r for r in csv.DictReader(stream)}
    with (root / 'observations.csv').open(newline='', encoding='utf-8-sig') as stream:
        records = [validate_row(row, prototypes, sources) for row in csv.DictReader(stream)]
    if len({r['id'] for r in records}) != len(records):
        raise ValueError('Duplicate observation IDs')
    dataset = dict(schema='technical-vehicle-operations-dataset/1', version=VERSION,
                   id='dataset.vehicle.operations', date='2026-10-08',
                   policy='Source observations and explicit scenario inputs; no automatic price, interval, wear-life or failure-rate adoption.',
                   sources=sources_document['sources'], records=records)
    (root / 'dataset.json').write_text(json.dumps(dataset, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
    with (root / 'coverage.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['prototype_id', 'exact_price_records', 'related_price_records', 'exact_service_records', 'other_records', 'gaps'])
        for pid in prototypes:
            own = [r for r in records if r['subject']['prototypeId'] == pid]
            exact_prices = sum(r['metric'] == 'vehicle_price' and r['subject']['matchStatus'] == 'exact-source-variant' for r in own)
            related_prices = sum(r['metric'] == 'vehicle_price' and r['subject']['matchStatus'] != 'exact-source-variant' for r in own)
            services = sum(r['metric'].endswith('_interval') and r['subject']['matchStatus'] == 'exact-source-variant' for r in own)
            gaps = [name for name, present in [('exact price', exact_prices), ('OEM service schedule', services),
                     ('axle-specific tyre lifetime', False), ('variant-specific repair probability/downtime', False)] if not present]
            writer.writerow([pid, exact_prices, related_prices, services, len(own), '; '.join(gaps)])
    files = {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob('*'))
             if p.is_file() and '__pycache__' not in p.parts and p.name not in {'release.json', 'test_operations.py'}}
    release = dict(schema='technical-vehicle-operations-release/1', version=VERSION,
                   datasetId='dataset.vehicle.operations', files=files,
                   prototypeRegistry=dict(path='vehicles/vehicle_prototypes.csv', sha256=sha(root.parent / 'vehicle_prototypes.csv')))
    (root / 'release.json').write_text(json.dumps(release, indent=2) + '\n')
    print(json.dumps(dict(version=VERSION, records=len(records), sources=len(sources), prototypes=len(prototypes))))
    return dataset


if __name__ == '__main__':
    build()
