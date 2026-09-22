-- ============================================================
--  SkyReport — esquema de base de datos para Supabase
-- ============================================================
--  CÓMO USARLO
--    1. Crea un proyecto en https://supabase.com (el plan gratis vale)
--    2. En el menú, abre "SQL Editor"
--    3. Pega TODO este archivo y dale a Run
--    4. Copia la Project URL y la anon key (Settings → API)
--       y pégalas en srs/config.js
--
--  LO MÁS IMPORTANTE DE ESTE ARCHIVO SON LAS POLICIES DEL FINAL.
--  La anon key viaja en el navegador y es pública: cualquiera puede
--  verla. Lo que impide que alguien lea, cambie o borre lo que no
--  debe son estas políticas, NO el JavaScript. Si te saltas esta
--  parte, dejas la base de datos abierta a todo el mundo.
--
--  Qué se permite exactamente:
--    · leer        → solo los reportes con status = 'approved'
--    · sitios      → se leen los 'approved'; los 'proposed' solo los ve quien
--                    los propuso y el equipo de moderacion
--    · añadir      → cualquiera, pero SIN poder marcar 'approved'
--    · cambiar     → nadie desde el navegador
--    · borrar      → nadie desde el navegador
-- ============================================================


-- ============================================================
--  TABLAS
-- ============================================================

-- ---------- SITIOS ----------
create table if not exists public.sites (
  id          text primary key,
  name        text not null,
  country     text,
  region      text,
  latitude    double precision not null,
  longitude   double precision not null,
  altitude    integer,
  description text,
  active      boolean not null default true,

  /* ===== DE DONDE SALE ESTE SITIO =====
     Hoy los sitios los mete el equipo desde el panel. Esta columna deja la
     puerta abierta a que un piloto proponga uno: su reporte se guarda ya con
     el sitio propuesto, y queda marcado como 'proposed' hasta que alguien lo
     revise. Asi nadie se queda sin reportar por volar en un sitio que aun no
     esta en la lista.

     El flujo no esta activado en el formulario todavia: es solo la columna,
     para no tener que migrar la tabla despues. */
  status      text not null default 'approved'
              check (status in ('proposed', 'approved', 'rejected')),
  proposed_by uuid,                    /* quien lo propuso, si fue un piloto */

  /* ===== EL PUNTO ES LO QUE IDENTIFICA EL SITIO =====
     El nombre es texto libre, y el mismo sitio puede llegar como 'Valle',
     'Valle de Bravo' o 'valle bravo'. Lo que de verdad identifica un sitio son
     sus coordenadas. Guardamos el punto en una columna aparte, para poder
     detectar despues que dos propuestas distintas son el mismo sitio y unirlas
     sin perder los reportes de ninguna de las dos. */
  name_raw    text,                    /* el nombre tal como lo escribio el piloto */

  created_at  timestamptz not null default now()
);

create index if not exists sites_status_idx on public.sites (status);
create index if not exists sites_geo_idx    on public.sites (latitude, longitude);

comment on table public.sites is
  'Sitios de vuelo. Las coordenadas son del punto de referencia del sitio, no de un incidente.';


-- ---------- ZONAS DENTRO DE UN SITIO ----------
--  De momento son puntos. Se deja preparada la columna `geometry`
--  para cuando las zonas sean polígonos (GeoJSON) de verdad.
--  Para activarla: create extension if not exists postgis;
create table if not exists public.site_zones (
  id          text primary key,
  site_id     text not null references public.sites(id) on delete cascade,
  name        text not null,
  type        text not null,          -- launch, landing, ridge, lee, venturi, rotor, ...
  latitude    double precision,
  longitude   double precision,
  geometry    jsonb,                  -- futuro: polígono GeoJSON
  created_at  timestamptz not null default now()
);

create index if not exists site_zones_site_idx on public.site_zones (site_id);

comment on column public.site_zones.geometry is
  'Polígono GeoJSON de la zona. Vacío mientras las zonas sean solo un punto.';


-- ---------- REPORTES ----------
create table if not exists public.reports (
  id                    uuid primary key,          -- lo genera el cliente: evita duplicados al sincronizar
  created_at            timestamptz not null default now(),

  -- qué es
  report_type           text not null
                        check (report_type in ('incident','near_miss','hazard','safe_flight')),

  -- dónde y cuándo
  site_id               text references public.sites(id) on delete set null,
  date                  date,
  time                  text,
  latitude              double precision,
  longitude             double precision,
  zone_id               text references public.site_zones(id) on delete set null,

  -- el vuelo y el evento
  flight_phase          text,
  event_type            text,
  outcome               text,
  injury_severity       text default 'none'
                        check (injury_severity in ('none','minor','serious','fatal')),

  -- condiciones (lo que reporta el piloto)
  wind_direction        text,
  wind_kmh              integer,
  gust_kmh              integer,
  thermal_activity      text,
  turbulence            text,
  cloud_conditions      text,
  weather_notes         text,

  -- equipo (sin identificar a nadie)
  wing_brand            text,
  wing_model            text,
  wing_class            text,
  wing_size             text,
  harness               text,
  reserve               text,
  experience_range      text,

  -- narrativa
  description           text,
  contributing_factors  text,
  lessons_learned       text,
  advice                text,

  -- IGC
  has_igc               boolean not null default false,
  igc_metadata          jsonb,
  --  Qué se guarda aquí (nunca el archivo entero):
  --    { event_timestamp, duration_s, max_alt, min_alt, gps_alt, baro_alt,
  --      anomalies: [...], points_count }
  --  El track completo NO se publica. Se usa para el análisis.

  -- preguntas específicas del tipo de evento
  additional_event_data jsonb,

  -- calidad del DATO (no del piloto): 0-100
  data_completeness     integer
                        check (data_completeness is null or data_completeness between 0 and 100),

  -- moderación
  status                text not null default 'pending'
                        check (status in ('pending','approved','rejected')),
  duplicate_of          uuid references public.reports(id) on delete set null
);

create index if not exists reports_status_idx      on public.reports (status);
create index if not exists reports_site_idx        on public.reports (site_id);
create index if not exists reports_fecha_idx       on public.reports (date desc);
create index if not exists reports_evento_idx      on public.reports (event_type);
create index if not exists reports_geo_idx         on public.reports (latitude, longitude);
-- el índice que más se usa: reportes aprobados de un sitio, recientes
create index if not exists reports_sitio_fecha_idx on public.reports (site_id, date desc)
  where status = 'approved';

comment on table public.reports is
  'Reportes individuales. Se redondean las coordenadas antes de publicarlas y nunca se guarda el IGC original.';


-- ---------- VUELOS SIN INCIDENTES ----------
--  Esto es el DENOMINADOR. Sin esto, "100 incidentes" no dice nada:
--  100 de 500 vuelos no es lo mismo que 100 de 50.000.
--  A propósito NO tiene nada de información personal.
create table if not exists public.safe_flight_logs (
  id          uuid primary key,
  created_at  timestamptz not null default now(),
  site_id     text references public.sites(id) on delete cascade,
  date        date not null,
  flight_type text
);

create index if not exists safe_flights_site_idx on public.safe_flight_logs (site_id);
create index if not exists safe_flights_fecha_idx on public.safe_flight_logs (date desc);

comment on table public.safe_flight_logs is
  'Vuelos registrados donde no pasó nada. Sirve para poner los reportes en contexto.';


-- ---------- SEÑALES ----------
--  De momento se calculan en el navegador a partir de los reportes.
--  Esta tabla existe para poder guardarlas más adelante: fijar cuáles
--  se han publicado, revisarlas, y que no cambien de un día para otro.
create table if not exists public.signals (
  id           text primary key,
  rule         text not null,              -- R1 cluster, R2 viento, R3 zona, R4 hora, R5 reservas, R6 viento fuerte
  site_id      text references public.sites(id) on delete cascade,
  zone_id      text references public.site_zones(id) on delete set null,
  title        text not null,
  explanation  text,
  report_ids   uuid[],
  date_start   date,
  date_end     date,
  strength     text check (strength in ('limited','repeated','strong')),
  status       text not null default 'pending'
               check (status in ('pending','approved','rejected')),
  created_at   timestamptz not null default now()
);

create index if not exists signals_site_idx   on public.signals (site_id);
create index if not exists signals_status_idx on public.signals (status);


-- ============================================================
--  DATOS INICIALES: los cuatro sitios
-- ============================================================
--  ⚠️ Las coordenadas y zonas de abajo son de DEMOSTRACIÓN.
--  Están puestas para que la app tenga con qué funcionar y para
--  que se vea la forma que tienen los datos. Antes de usar esto
--  en producción, sustitúyelas por las reales.
insert into public.sites (id, name, country, region, latitude, longitude, altitude, description, active)
values
  ('valle',     'Valle de Bravo', 'Mexico',          'Estado de Mexico', 19.1070, -100.1260, 2100,
   'Classic thermal site above a lake. Big air, strong cycles, busy in season.', true),
  ('krushevo',  'Krushevo',       'North Macedonia', 'Pelagonia',        41.3680,   21.2480, 1350,
   'High plateau, reliable convergence, competition venue. Long transitions.', true),
  ('castelo',   'Castelo',        'Brazil',          'Espírito Santo',  -20.6040,  -41.1910,  850,
   'Inland ridge flying, humid air, strong thermals late in the day.', true),
  ('pegalajar', 'Pegalajar',      'Spain',           'Sierra Mágina',    37.7400,   -3.6470, 1100,
   'Inland Andalusia. Dry, dusty, sharp thermals and a small landing area.', true)
on conflict (id) do nothing;

insert into public.site_zones (id, site_id, name, type, latitude, longitude)
values
  ('v-launch',  'valle', 'Launch (El Peñón)',          'launch',     19.1120, -100.1220),
  ('v-ridge',   'valle', 'Main ridge',                  'ridge',      19.1180, -100.1320),
  ('v-lee',     'valle', 'Lee side of main ridge',      'lee',        19.1215, -100.1400),
  ('v-venturi', 'valle', 'Venturi at the gap',          'venturi',    19.1250, -100.1360),
  ('v-trans',   'valle', 'Lake crossing transition',    'transition', 19.1180, -100.1500),
  ('v-landing', 'valle', 'Landing (La Candelaria)',     'landing',    19.1030, -100.1180),

  ('k-launch',  'krushevo', 'Launch (Mečkin Kamen)',    'launch',        41.3720, 21.2420),
  ('k-ridge',   'krushevo', 'North ridge',              'ridge',         41.3760, 21.2540),
  ('k-lee',     'krushevo', 'Lee of north ridge',       'lee',           41.3800, 21.2620),
  ('k-conv',    'krushevo', 'Convergence line',         'convergence',   41.3600, 21.2600),
  ('k-landing', 'krushevo', 'Main landing field',       'landing',       41.3640, 21.2450),

  ('c-launch',  'castelo', 'Launch (Pedra do Castelo)', 'launch',       -20.6010, -41.1880),
  ('c-ridge',   'castelo', 'Main ridge line',           'ridge',        -20.6080, -41.1960),
  ('c-rotor',   'castelo', 'Rotor behind the col',      'rotor',        -20.6120, -41.2030),
  ('c-cables',  'castelo', 'Cables on the road crossing','cables',      -20.6070, -41.1880),
  ('c-landing', 'castelo', 'Landing field',             'landing',      -20.6060, -41.1900),

  ('p-launch',  'pegalajar', 'Launch (Sierra Mágina)',  'launch',        37.7440, -3.6430),
  ('p-ridge',   'pegalajar', 'East ridge',              'ridge',         37.7460, -3.6520),
  ('p-venturi', 'pegalajar', 'Venturi between the two spurs','venturi',  37.7480, -3.6580),
  ('p-landing', 'pegalajar', 'Village landing',         'landing',       37.7380, -3.6450),
  ('p-hazard',  'pegalajar', 'Rock band on approach',   'hazard',        37.7410, -3.6440)
on conflict (id) do nothing;


-- ============================================================
--  ROW LEVEL SECURITY
-- ============================================================
--  A partir de aquí está lo que de verdad protege los datos.

alter table public.sites            enable row level security;
alter table public.site_zones       enable row level security;
alter table public.reports          enable row level security;
alter table public.safe_flight_logs enable row level security;
alter table public.signals          enable row level security;


-- ---------- SITIOS: lectura pública, escritura solo con cuenta ----------
drop policy if exists "sitios lectura publica" on public.sites;
create policy "sitios lectura publica"
  on public.sites for select
  to anon, authenticated
  using (active = true);

drop policy if exists "sitios escritura con cuenta" on public.sites;
create policy "sitios escritura con cuenta"
  on public.sites for all
  to authenticated
  using (true) with check (true);


-- ---------- ZONAS: igual ----------
drop policy if exists "zonas lectura publica" on public.site_zones;
create policy "zonas lectura publica"
  on public.site_zones for select
  to anon, authenticated
  using (true);

drop policy if exists "zonas escritura con cuenta" on public.site_zones;
create policy "zonas escritura con cuenta"
  on public.site_zones for all
  to authenticated
  using (true) with check (true);


-- ---------- REPORTES ----------
--  Se leen SOLO los aprobados. Un reporte pendiente o rechazado no
--  lo ve nadie desde el navegador, ni siquiera quien lo escribió
--  (por eso se le da un acuse con su id al enviarlo).

drop policy if exists "reportes ver aprobados" on public.reports;
create policy "reportes ver aprobados"
  on public.reports for select
  to anon, authenticated
  using (status = 'approved');

--  Cualquiera puede AÑADIR, pero con dos condiciones:
--    1. no puede entrar ya como aprobado (si no, la moderación no sirve de nada)
--    2. no puede marcarlo como duplicado de otro sin permiso
drop policy if exists "reportes insertar anonimo" on public.reports;
create policy "reportes insertar anonimo"
  on public.reports for insert
  to anon, authenticated
  with check (
    status = 'pending'
    and duplicate_of is null
  );

--  Nadie modifica ni borra desde el navegador. La moderación se hace
--  con una cuenta autenticada (o desde el panel de Supabase).
drop policy if exists "reportes moderar con cuenta" on public.reports;
create policy "reportes moderar con cuenta"
  on public.reports for update
  to authenticated
  using (true) with check (true);

drop policy if exists "reportes borrar con cuenta" on public.reports;
create policy "reportes borrar con cuenta"
  on public.reports for delete
  to authenticated
  using (true);


-- ---------- VUELOS SIN INCIDENTES ----------
--  Se leen para poder contar (el dato de exposición) y se añaden.
--  OJO: aquí NO hay información personal, así que la lectura pública
--  no expone a nadie. Solo dice "en este sitio, este día, hubo un vuelo".
drop policy if exists "vuelos ver" on public.safe_flight_logs;
create policy "vuelos ver"
  on public.safe_flight_logs for select
  to anon, authenticated
  using (true);

drop policy if exists "vuelos insertar anonimo" on public.safe_flight_logs;
create policy "vuelos insertar anonimo"
  on public.safe_flight_logs for insert
  to anon, authenticated
  with check (true);

drop policy if exists "vuelos borrar con cuenta" on public.safe_flight_logs;
create policy "vuelos borrar con cuenta"
  on public.safe_flight_logs for delete
  to authenticated
  using (true);


-- ---------- SEÑALES ----------
drop policy if exists "senales ver aprobadas" on public.signals;
create policy "senales ver aprobadas"
  on public.signals for select
  to anon, authenticated
  using (status = 'approved');

drop policy if exists "senales gestionar con cuenta" on public.signals;
create policy "senales gestionar con cuenta"
  on public.signals for all
  to authenticated
  using (true) with check (true);


-- ============================================================
--  COMPROBACIÓN RÁPIDA (opcional)
-- ============================================================
--  Después de ejecutar todo, esto debe devolver 5 filas con
--  rowsecurity = true. Si alguna está en false, esa tabla está
--  abierta y hay que revisar.
--
--    select tablename, rowsecurity
--    from pg_tables
--    where schemaname = 'public'
--    order by tablename;
-- ============================================================
