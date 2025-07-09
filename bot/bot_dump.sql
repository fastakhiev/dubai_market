--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.4 (Debian 17.4-1.pgdg120+2)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: meta_db_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO meta_db_user;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: meta_db_user
--

CREATE TABLE public.orders (
    id uuid NOT NULL,
    product_id uuid NOT NULL,
    buyer_id uuid NOT NULL,
    destination character varying NOT NULL,
    seller_comment character varying,
    buyer_comment character varying,
    is_approve boolean NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.orders OWNER TO meta_db_user;

--
-- Name: products; Type: TABLE; Schema: public; Owner: meta_db_user
--

CREATE TABLE public.products (
    id uuid NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    price numeric(10,2) NOT NULL,
    currency character varying(10) NOT NULL,
    seller_id uuid NOT NULL,
    status character varying(50) NOT NULL,
    photos json,
    thumbnail character varying,
    category character varying(100) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.products OWNER TO meta_db_user;

--
-- Name: questions; Type: TABLE; Schema: public; Owner: meta_db_user
--

CREATE TABLE public.questions (
    id uuid NOT NULL,
    buyer_id uuid NOT NULL,
    product_id uuid NOT NULL,
    question character varying NOT NULL,
    answer character varying,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.questions OWNER TO meta_db_user;

--
-- Name: shops; Type: TABLE; Schema: public; Owner: meta_db_user
--

CREATE TABLE public.shops (
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    photo character varying(100) NOT NULL,
    social_networks character varying(1000),
    user_id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.shops OWNER TO meta_db_user;

--
-- Name: users; Type: TABLE; Schema: public; Owner: meta_db_user
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    telegram_id character varying(100) NOT NULL,
    full_name character varying(100) NOT NULL,
    phone character varying(50) NOT NULL,
    role character varying(50) NOT NULL,
    passport character varying(1000),
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.users OWNER TO meta_db_user;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: meta_db_user
--

COPY public.alembic_version (version_num) FROM stdin;
67fc71fd38ec
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: meta_db_user
--

COPY public.orders (id, product_id, buyer_id, destination, seller_comment, buyer_comment, is_approve, created_at) FROM stdin;
e9ddb423-523c-4fc7-b1df-745abd963840	0bbe1d4c-1fdb-46a5-9a74-4920c0ea87fd	a4b003d9-b577-42a5-a10c-bd076c470b56	Татар базар	Да гей, вопросы?	Султан гей	t	2025-05-17 06:20:25.466257
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: meta_db_user
--

COPY public.products (id, title, description, price, currency, seller_id, status, photos, thumbnail, category, created_at, updated_at) FROM stdin;
4cb41d73-fda9-40a8-ac65-3c5740e8762c	Товар 1	Тест товар 1	12.00	AED	8b24f637-a0ba-42f4-bcef-f2b8e91cbd52	active	["AgACAgIAAxkBAAIM9GgabuK1bdCIqnCM9M8l9OyVhQulAAIC8zEbMjnQSOS4ZMjdnX4HAQADAgADeQADNgQ", "AgACAgIAAxkBAAIM9WgabuLGoRQDpWUc2tg70ZCSPykxAAID8zEbMjnQSJjF5K8e6rx8AQADAgADeQADNgQ", "AgACAgIAAxkBAAIM9mgabuIT3HoAASy_An8wOPv5XkyXvQACkAABMhvejtFIsoQmSSQBJHsBAAMCAAN5AAM2BA"]	AgACAgIAAxkBAAIM9GgabuK1bdCIqnCM9M8l9OyVhQulAAIC8zEbMjnQSOS4ZMjdnX4HAQADAgADeQADNgQ	Дом и сад	2025-05-06 19:35:45.980901	2025-05-06 19:35:45.98096
0319d122-b182-41fd-afc7-30c63e545bd8	Дубайский шоколад	В продаже дубайский шоколад FIX	79.00	AED	677f194d-52b0-4dc5-9931-0b76c75d1bd0	active	["AgACAgQAAxkBAAINdWgl3haie24Ejz3ZkyyP33Z34DGzAAKbyTEb1awwUaFPtBtAlJTEAQADAgADbQADNgQ"]	AgACAgQAAxkBAAINdWgl3haie24Ejz3ZkyyP33Z34DGzAAKbyTEb1awwUaFPtBtAlJTEAQADAgADbQADNgQ	Одежда, обувь и аксессуары	2025-05-12 13:45:48.080551	2025-05-12 13:45:48.080613
0bbe1d4c-1fdb-46a5-9a74-4920c0ea87fd	Тест 2	Тест 2	12.00	USD	8b24f637-a0ba-42f4-bcef-f2b8e91cbd52	active	["AgACAgIAAxkBAAINr2gmG_PuAfxlO05OnJoTibeE4mQIAAKj7zEblUQ4SdB7msEpvfxhAQADAgADeQADNgQ"]	AgACAgIAAxkBAAINr2gmG_PuAfxlO05OnJoTibeE4mQIAAKj7zEblUQ4SdB7msEpvfxhAQADAgADeQADNgQ	Красота и здоровье	2025-05-15 16:50:09.070226	2025-05-15 16:50:09.070294
\.


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: meta_db_user
--

COPY public.questions (id, buyer_id, product_id, question, answer, created_at) FROM stdin;
6baeff39-60e7-4b7f-b2ba-773aa6ec317f	298274ef-df03-4063-973f-c2c2a068a568	4cb41d73-fda9-40a8-ac65-3c5740e8762c	Норм?	Норм	2025-05-06 20:21:17.093957
a59908b2-2b72-4bb6-9ad7-82d0e6e37722	a4b003d9-b577-42a5-a10c-bd076c470b56	0319d122-b182-41fd-afc7-30c63e545bd8	Султан гей ?	\N	2025-05-15 17:01:52.530739
f3b6e7cf-c6a9-46d3-bfc5-26d4fb2aa2de	a4b003d9-b577-42a5-a10c-bd076c470b56	0319d122-b182-41fd-afc7-30c63e545bd8	Султан гей ?	\N	2025-05-15 17:02:59.351484
32e76f80-4034-437f-8692-3230d87aea4f	298274ef-df03-4063-973f-c2c2a068a568	0bbe1d4c-1fdb-46a5-9a74-4920c0ea87fd	Да?	Да	2025-05-17 02:50:57.112555
060b7b0d-0fc4-47bd-b164-b638408d346a	8309bc59-6f9e-4a4f-b21f-14dd4a5d5205	4cb41d73-fda9-40a8-ac65-3c5740e8762c	Антон?	Да	2025-05-17 06:24:04.158038
928c2cc0-d635-4f1a-842c-9b68cf0a5401	8309bc59-6f9e-4a4f-b21f-14dd4a5d5205	0bbe1d4c-1fdb-46a5-9a74-4920c0ea87fd	Антон?	Нет	2025-05-17 06:23:22.381806
\.


--
-- Data for Name: shops; Type: TABLE DATA; Schema: public; Owner: meta_db_user
--

COPY public.shops (id, name, photo, social_networks, user_id, created_at) FROM stdin;
c4f5f768-482a-452b-b2af-507ee2ab0cee	Тест шоп	AgACAgIAAxkBAAIM3mgaaFCkcpEvmju4IHxehfXjGNJ0AAK88jEbMjnQSPOVSPfB0fSgAQADAgADeQADNgQ	@test	8b24f637-a0ba-42f4-bcef-f2b8e91cbd52	2025-05-06 19:51:44.916829
dc4a3d03-e470-4632-b2a9-7aefada1af4e	Султан	AgACAgQAAxkBAAINaWgl3O3ys3SYgrYVPJrjwAcRjDDYAAKXyTEb1awwUWoEi-PKzLeyAQADAgADeQADNgQ	Введите ссылку на социальные сети вашего магазина, в случае если их нет, то нажмите кнопку «Пропустить»	677f194d-52b0-4dc5-9931-0b76c75d1bd0	2025-05-15 12:24:13.629553
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: meta_db_user
--

COPY public.users (id, telegram_id, full_name, phone, role, passport, created_at) FROM stdin;
8b24f637-a0ba-42f4-bcef-f2b8e91cbd52	587764139	Тест	123	seller	AgACAgIAAxkBAAIM12gaaDqA7pB_0upjG_uIuc96uFZiAAK-8TEbFUTRSGARDQmv6MD9AQADAgADeQADNgQ	2025-05-06 19:51:22.193059
298274ef-df03-4063-973f-c2c2a068a568	7213351883	Тест покупатель	362819	buyer	\N	2025-05-06 20:20:37.889445
a4b003d9-b577-42a5-a10c-bd076c470b56	899420796	Марсель	89124485555	buyer	\N	2025-05-07 13:19:36.967075
677f194d-52b0-4dc5-9931-0b76c75d1bd0	8097143576	Продавец 🧑‍💼	55555555555	seller	AgACAgQAAxkBAAINYmgl3CO1SDVcahASUnhiFFe53IasAAKQyTEb1awwUWUXrX4p6ZbLAQADAgADeQADNgQ	2025-05-15 12:20:51.35613
640411a1-aa36-4c61-8b16-80bbc5cabd2c	8130864584	Евгений Онегин	+971549986697	buyer	\N	2025-05-15 16:29:36.449548
8309bc59-6f9e-4a4f-b21f-14dd4a5d5205	8011067934	Андрей	473919	buyer	\N	2025-05-17 06:23:01.419593
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- Name: shops shops_pkey; Type: CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.shops
    ADD CONSTRAINT shops_pkey PRIMARY KEY (id);


--
-- Name: shops shops_user_id_key; Type: CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.shops
    ADD CONSTRAINT shops_user_id_key UNIQUE (user_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_telegram_id_key; Type: CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_telegram_id_key UNIQUE (telegram_id);


--
-- Name: orders orders_buyer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_buyer_id_fkey FOREIGN KEY (buyer_id) REFERENCES public.users(id);


--
-- Name: orders orders_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: products products_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.users(id);


--
-- Name: questions questions_buyer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_buyer_id_fkey FOREIGN KEY (buyer_id) REFERENCES public.users(id);


--
-- Name: questions questions_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: shops shops_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meta_db_user
--

ALTER TABLE ONLY public.shops
    ADD CONSTRAINT shops_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

