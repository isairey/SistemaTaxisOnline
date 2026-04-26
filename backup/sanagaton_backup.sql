--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-11-06 01:57:39

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4951 (class 1262 OID 16970)
-- Name: taxi; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE taxi WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'es-ES';


ALTER DATABASE taxi OWNER TO postgres;

\connect taxi

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 6 (class 2615 OID 17471)
-- Name: sanagaton; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA sanagaton;


ALTER SCHEMA sanagaton OWNER TO postgres;

--
-- TOC entry 858 (class 1247 OID 17473)
-- Name: rol_enum; Type: TYPE; Schema: sanagaton; Owner: postgres
--

CREATE TYPE sanagaton.rol_enum AS ENUM (
    'admin',
    'user',
    'guest'
);


ALTER TYPE sanagaton.rol_enum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 223 (class 1259 OID 17503)
-- Name: avances; Type: TABLE; Schema: sanagaton; Owner: postgres
--

CREATE TABLE sanagaton.avances (
    id_avance integer NOT NULL,
    numero_control integer,
    nombre character varying(60),
    apellido character varying(60),
    fecha_nacimiento date,
    rif character varying(20),
    documento_avance character varying(20),
    numero_telf character varying(20)
);


ALTER TABLE sanagaton.avances OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 17502)
-- Name: avances_id_avance_seq; Type: SEQUENCE; Schema: sanagaton; Owner: postgres
--

ALTER TABLE sanagaton.avances ALTER COLUMN id_avance ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sanagaton.avances_id_avance_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 227 (class 1259 OID 17525)
-- Name: finanzas; Type: TABLE; Schema: sanagaton; Owner: postgres
--

CREATE TABLE sanagaton.finanzas (
    id_finanzas integer NOT NULL,
    documento character varying(20) NOT NULL,
    pagos_mensuales numeric(10,2),
    impuestos_anuales numeric(10,2),
    fecha_pago date,
    numero_contr character varying(3)
);


ALTER TABLE sanagaton.finanzas OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 17524)
-- Name: finanzas_id_finanzas_seq; Type: SEQUENCE; Schema: sanagaton; Owner: postgres
--

ALTER TABLE sanagaton.finanzas ALTER COLUMN id_finanzas ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sanagaton.finanzas_id_finanzas_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 221 (class 1259 OID 17492)
-- Name: sanciones; Type: TABLE; Schema: sanagaton; Owner: postgres
--

CREATE TABLE sanagaton.sanciones (
    id_sancion integer NOT NULL,
    documento character varying(20) NOT NULL,
    motivo_sancion character varying(255),
    monto numeric(10,2),
    inicio_sancion date,
    final_sancion date,
    nombre character varying(45),
    apellido character varying(45)
);


ALTER TABLE sanagaton.sanciones OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 17491)
-- Name: sanciones_id_sancion_seq; Type: SEQUENCE; Schema: sanagaton; Owner: postgres
--

ALTER TABLE sanagaton.sanciones ALTER COLUMN id_sancion ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sanagaton.sanciones_id_sancion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 219 (class 1259 OID 17480)
-- Name: socio; Type: TABLE; Schema: sanagaton; Owner: postgres
--

CREATE TABLE sanagaton.socio (
    id_socio integer NOT NULL,
    documento character varying(20) NOT NULL,
    nombres character varying(60) NOT NULL,
    apellidos character varying(60) NOT NULL,
    direccion character varying(255),
    numero_telefono character varying(15),
    numero_control integer,
    rif character varying(20),
    fecha_nacimiento date
);


ALTER TABLE sanagaton.socio OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 17479)
-- Name: socio_id_socio_seq; Type: SEQUENCE; Schema: sanagaton; Owner: postgres
--

ALTER TABLE sanagaton.socio ALTER COLUMN id_socio ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sanagaton.socio_id_socio_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 229 (class 1259 OID 17542)
-- Name: usuarios; Type: TABLE; Schema: sanagaton; Owner: postgres
--

CREATE TABLE sanagaton.usuarios (
    id_usuario integer NOT NULL,
    nombre_usuario character varying(50),
    password character varying(100),
    rol sanagaton.rol_enum
);


ALTER TABLE sanagaton.usuarios OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 17541)
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE; Schema: sanagaton; Owner: postgres
--

ALTER TABLE sanagaton.usuarios ALTER COLUMN id_usuario ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sanagaton.usuarios_id_usuario_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 225 (class 1259 OID 17514)
-- Name: vehiculos; Type: TABLE; Schema: sanagaton; Owner: postgres
--

CREATE TABLE sanagaton.vehiculos (
    id_vehiculo integer NOT NULL,
    documento character varying(20) NOT NULL,
    numero_control integer,
    marca character varying(50),
    modelo character varying(50),
    ano integer,
    placa character varying(10)
);


ALTER TABLE sanagaton.vehiculos OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 17513)
-- Name: vehiculos_id_vehiculo_seq; Type: SEQUENCE; Schema: sanagaton; Owner: postgres
--

ALTER TABLE sanagaton.vehiculos ALTER COLUMN id_vehiculo ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sanagaton.vehiculos_id_vehiculo_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 4939 (class 0 OID 17503)
-- Dependencies: 223
-- Data for Name: avances; Type: TABLE DATA; Schema: sanagaton; Owner: postgres
--

INSERT INTO sanagaton.avances (id_avance, numero_control, nombre, apellido, fecha_nacimiento, rif, documento_avance, numero_telf) OVERRIDING SYSTEM VALUE VALUES (5, 2, 'Alexander', 'Redondo', '2005-06-05', 'V123445678', 'V-5663855', '4160161789');
INSERT INTO sanagaton.avances (id_avance, numero_control, nombre, apellido, fecha_nacimiento, rif, documento_avance, numero_telf) OVERRIDING SYSTEM VALUE VALUES (2, 1, 'Isaac', 'Pabon', '2003-04-06', 'V12345689', 'V-28306182', '4142132775');
INSERT INTO sanagaton.avances (id_avance, numero_control, nombre, apellido, fecha_nacimiento, rif, documento_avance, numero_telf) OVERRIDING SYSTEM VALUE VALUES (8, 4, 'Rigoberto', 'Rosales', '2005-04-11', 'V1425612', 'V-1616112', '4142132775');


--
-- TOC entry 4943 (class 0 OID 17525)
-- Dependencies: 227
-- Data for Name: finanzas; Type: TABLE DATA; Schema: sanagaton; Owner: postgres
--

INSERT INTO sanagaton.finanzas (id_finanzas, documento, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr) OVERRIDING SYSTEM VALUE VALUES (4, 'V-1616112', 14.05, 130.10, '2025-04-21', '05');
INSERT INTO sanagaton.finanzas (id_finanzas, documento, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr) OVERRIDING SYSTEM VALUE VALUES (5, 'V-5663855', 130.06, 145.05, '2025-08-10', '10');
INSERT INTO sanagaton.finanzas (id_finanzas, documento, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr) OVERRIDING SYSTEM VALUE VALUES (3, 'V-1616112', 123.34, 123.90, '2025-04-30', '04');


--
-- TOC entry 4937 (class 0 OID 17492)
-- Dependencies: 221
-- Data for Name: sanciones; Type: TABLE DATA; Schema: sanagaton; Owner: postgres
--

INSERT INTO sanagaton.sanciones (id_sancion, documento, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido) OVERRIDING SYSTEM VALUE VALUES (1, 'V-28306182', 'Exceso de velocidad y estaba borracho', 114.50, '2025-09-10', '2025-10-28', 'Javier', 'Pabón');
INSERT INTO sanagaton.sanciones (id_sancion, documento, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido) OVERRIDING SYSTEM VALUE VALUES (3, 'V-5663855', 'Mal estacionado', 128.29, '2025-06-08', '2025-07-08', 'Haydee', 'Monsalve');


--
-- TOC entry 4935 (class 0 OID 17480)
-- Dependencies: 219
-- Data for Name: socio; Type: TABLE DATA; Schema: sanagaton; Owner: postgres
--

INSERT INTO sanagaton.socio (id_socio, documento, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento) OVERRIDING SYSTEM VALUE VALUES (2, 'V-5663855', 'Haydee', 'Monsalve', 'Barrio Obrero / Plaza los mangos', '4142132775', 2, 'V5663855', '1963-01-20');
INSERT INTO sanagaton.socio (id_socio, documento, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento) OVERRIDING SYSTEM VALUE VALUES (3, 'V-28306182', 'Javier', 'Pabón', 'Las Mercedes - entre calle 6 y 10', '4142132775', 1, 'V52152526', '2002-02-02');
INSERT INTO sanagaton.socio (id_socio, documento, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento) OVERRIDING SYSTEM VALUE VALUES (10, 'V-8920352', 'Luis', 'Quevedo', 'Valencia', '4244041464', 15, 'V008920352', '1965-02-10');
INSERT INTO sanagaton.socio (id_socio, documento, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento) OVERRIDING SYSTEM VALUE VALUES (4, 'V-13897188', 'Tirza', 'Améstica', 'Las Lomas - San Cristobal', '4140151090', 3, 'V54218281', '1980-07-12');
INSERT INTO sanagaton.socio (id_socio, documento, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento) OVERRIDING SYSTEM VALUE VALUES (11, 'V-8556987', 'Haydee ', 'Monsalve', 'Urbanización', '4142137567', 23, 'V123344920', '1970-04-05');
INSERT INTO sanagaton.socio (id_socio, documento, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento) OVERRIDING SYSTEM VALUE VALUES (12, 'V-27114251', 'Emanuel', 'Amestica', 'Final calle 14 casa N0-49', '4247083636', 27, 'V27114251', '1999-08-27');
INSERT INTO sanagaton.socio (id_socio, documento, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento) OVERRIDING SYSTEM VALUE VALUES (6, 'V-1616112', 'Nancy', 'Amestica', 'Avenida', '414141411', 4, 'V12322234', '2003-02-05');


--
-- TOC entry 4945 (class 0 OID 17542)
-- Dependencies: 229
-- Data for Name: usuarios; Type: TABLE DATA; Schema: sanagaton; Owner: postgres
--

INSERT INTO sanagaton.usuarios (id_usuario, nombre_usuario, password, rol) OVERRIDING SYSTEM VALUE VALUES (1, 'Presidente', '$2b$12$L56pflFvR.CIwazkZqSoxeC9A1oUAuGeJl8gi4KmOGPLZ.kQ8Wn4m', 'admin');
INSERT INTO sanagaton.usuarios (id_usuario, nombre_usuario, password, rol) OVERRIDING SYSTEM VALUE VALUES (2, 'Secretario', '$2b$12$ga4MZRBd6IGVSO7pCR8gNeAVOn8hrumRydURR6L/hA2fAIDIuphQu', 'user');
INSERT INTO sanagaton.usuarios (id_usuario, nombre_usuario, password, rol) OVERRIDING SYSTEM VALUE VALUES (3, 'Tesorero', '$2b$12$QvASOLLuZhq6.FNPTGKYH.MA16nJy9PHTeLplwpWR0Py9vbhLmLpS', 'guest');


--
-- TOC entry 4941 (class 0 OID 17514)
-- Dependencies: 225
-- Data for Name: vehiculos; Type: TABLE DATA; Schema: sanagaton; Owner: postgres
--

INSERT INTO sanagaton.vehiculos (id_vehiculo, documento, numero_control, marca, modelo, ano, placa) OVERRIDING SYSTEM VALUE VALUES (1, 'V-28306182', 1, 'Corolla', 'toyota', 2005, 'ABC123');
INSERT INTO sanagaton.vehiculos (id_vehiculo, documento, numero_control, marca, modelo, ano, placa) OVERRIDING SYSTEM VALUE VALUES (9, 'V-5663855', 2, 'Corolla', 'Toyota', 2006, 'ABC4321');
INSERT INTO sanagaton.vehiculos (id_vehiculo, documento, numero_control, marca, modelo, ano, placa) OVERRIDING SYSTEM VALUE VALUES (12, 'V-1616112', 4, 'Bugatti', 'Vayron', 2010, 'XSDSAAAS');


--
-- TOC entry 4952 (class 0 OID 0)
-- Dependencies: 222
-- Name: avances_id_avance_seq; Type: SEQUENCE SET; Schema: sanagaton; Owner: postgres
--

SELECT pg_catalog.setval('sanagaton.avances_id_avance_seq', 10, true);


--
-- TOC entry 4953 (class 0 OID 0)
-- Dependencies: 226
-- Name: finanzas_id_finanzas_seq; Type: SEQUENCE SET; Schema: sanagaton; Owner: postgres
--

SELECT pg_catalog.setval('sanagaton.finanzas_id_finanzas_seq', 5, true);


--
-- TOC entry 4954 (class 0 OID 0)
-- Dependencies: 220
-- Name: sanciones_id_sancion_seq; Type: SEQUENCE SET; Schema: sanagaton; Owner: postgres
--

SELECT pg_catalog.setval('sanagaton.sanciones_id_sancion_seq', 3, true);


--
-- TOC entry 4955 (class 0 OID 0)
-- Dependencies: 218
-- Name: socio_id_socio_seq; Type: SEQUENCE SET; Schema: sanagaton; Owner: postgres
--

SELECT pg_catalog.setval('sanagaton.socio_id_socio_seq', 14, true);


--
-- TOC entry 4956 (class 0 OID 0)
-- Dependencies: 228
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE SET; Schema: sanagaton; Owner: postgres
--

SELECT pg_catalog.setval('sanagaton.usuarios_id_usuario_seq', 3, true);


--
-- TOC entry 4957 (class 0 OID 0)
-- Dependencies: 224
-- Name: vehiculos_id_vehiculo_seq; Type: SEQUENCE SET; Schema: sanagaton; Owner: postgres
--

SELECT pg_catalog.setval('sanagaton.vehiculos_id_vehiculo_seq', 12, true);


--
-- TOC entry 4778 (class 2606 OID 17507)
-- Name: avances avances_pkey; Type: CONSTRAINT; Schema: sanagaton; Owner: postgres
--

ALTER TABLE ONLY sanagaton.avances
    ADD CONSTRAINT avances_pkey PRIMARY KEY (id_avance);


--
-- TOC entry 4782 (class 2606 OID 17529)
-- Name: finanzas finanzas_pkey; Type: CONSTRAINT; Schema: sanagaton; Owner: postgres
--

ALTER TABLE ONLY sanagaton.finanzas
    ADD CONSTRAINT finanzas_pkey PRIMARY KEY (id_finanzas);


--
-- TOC entry 4776 (class 2606 OID 17496)
-- Name: sanciones sanciones_pkey; Type: CONSTRAINT; Schema: sanagaton; Owner: postgres
--

ALTER TABLE ONLY sanagaton.sanciones
    ADD CONSTRAINT sanciones_pkey PRIMARY KEY (id_sancion);


--
-- TOC entry 4772 (class 2606 OID 17488)
-- Name: socio socio_documento_key; Type: CONSTRAINT; Schema: sanagaton; Owner: postgres
--

ALTER TABLE ONLY sanagaton.socio
    ADD CONSTRAINT socio_documento_key UNIQUE (documento);


--
-- TOC entry 4774 (class 2606 OID 17486)
-- Name: socio socio_pkey; Type: CONSTRAINT; Schema: sanagaton; Owner: postgres
--

ALTER TABLE ONLY sanagaton.socio
    ADD CONSTRAINT socio_pkey PRIMARY KEY (id_socio);


--
-- TOC entry 4784 (class 2606 OID 17546)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: sanagaton; Owner: postgres
--

ALTER TABLE ONLY sanagaton.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 4780 (class 2606 OID 17518)
-- Name: vehiculos vehiculos_pkey; Type: CONSTRAINT; Schema: sanagaton; Owner: postgres
--

ALTER TABLE ONLY sanagaton.vehiculos
    ADD CONSTRAINT vehiculos_pkey PRIMARY KEY (id_vehiculo);


--
-- TOC entry 4786 (class 2606 OID 17508)
-- Name: avances fk_socio_avance; Type: FK CONSTRAINT; Schema: sanagaton; Owner: postgres
--

ALTER TABLE ONLY sanagaton.avances
    ADD CONSTRAINT fk_socio_avance FOREIGN KEY (documento_avance) REFERENCES sanagaton.socio(documento);


--
-- TOC entry 4788 (class 2606 OID 17530)
-- Name: finanzas fk_socio_finanzas; Type: FK CONSTRAINT; Schema: sanagaton; Owner: postgres
--

ALTER TABLE ONLY sanagaton.finanzas
    ADD CONSTRAINT fk_socio_finanzas FOREIGN KEY (documento) REFERENCES sanagaton.socio(documento);


--
-- TOC entry 4785 (class 2606 OID 17497)
-- Name: sanciones fk_socio_sanciones; Type: FK CONSTRAINT; Schema: sanagaton; Owner: postgres
--

ALTER TABLE ONLY sanagaton.sanciones
    ADD CONSTRAINT fk_socio_sanciones FOREIGN KEY (documento) REFERENCES sanagaton.socio(documento);


--
-- TOC entry 4787 (class 2606 OID 17519)
-- Name: vehiculos fk_socio_vehiculos; Type: FK CONSTRAINT; Schema: sanagaton; Owner: postgres
--

ALTER TABLE ONLY sanagaton.vehiculos
    ADD CONSTRAINT fk_socio_vehiculos FOREIGN KEY (documento) REFERENCES sanagaton.socio(documento);


-- Completed on 2025-11-06 01:57:39

--
-- PostgreSQL database dump complete
--

