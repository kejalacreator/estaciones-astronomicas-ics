# generate_ics.py
from skyfield import api, almanac
from datetime import datetime, timezone
from icalendar import Calendar, Event

def get_seasons_for_year(eph, ts, year):
    t0 = ts.utc(year, 1, 1)
    t1 = ts.utc(year, 12, 31)
    f = almanac.seasons(eph)
    times, events = almanac.find_discrete(t0, t1, f)
    names = [
        'Equinoccio de marzo - Primavera N / Otoño S',
        'Solsticio de junio - Verano N / Invierno S',
        'Equinoccio de septiembre - Otoño N / Primavera S',
        'Solsticio de diciembre - Invierno N / Verano S'
    ]
    return [(t.utc_datetime().replace(tzinfo=timezone.utc), names[e]) for t, e in zip(times, events)]

def make_ics(out_path='estaciones_america_preciso.ics', start_year=2025, end_year=2030):
    ts = api.load.timescale()
    eph = api.load('de421.bsp')

    cal = Calendar()
    cal.add('prodid', '-//TuOrg//Estaciones Américas Astronómicas//ES')
    cal.add('version', '2.0')
    cal.add('X-WR-CALNAME', 'Inicio de estaciones - Américas (Astronómico)')
    cal.add('X-WR-TIMEZONE', 'UTC')

    for year in range(start_year, end_year + 1):
        events = get_seasons_for_year(eph, ts, year)
        for dt_utc, name in events:
            ev = Event()
            uid = f"{name.replace(' ','-').lower()}-{year}@tu-org.org"
            ev.add('uid', uid)
            ev.add('dtstamp', datetime.now(timezone.utc))
            ev.add('dtstart', dt_utc)
            ev.add('summary', name)
            ev.add('description', f"{name} - instante astronómico (UTC)")
            cal.add_component(ev)

    with open(out_path, 'wb') as f:
        f.write(cal.to_ical())
    print(f"[OK] Archivo generado: {out_path}")

if __name__ == "__main__":
    make_ics(start_year=2025, end_year=2030)
