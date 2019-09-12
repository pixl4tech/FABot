
CREATE SEQUENCE public.schedule_id_row_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;
	
CREATE SEQUENCE public.schedule_id_row_seq1
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

CREATE SEQUENCE public.snap_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;
	
CREATE SEQUENCE public.user_ids
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

-- Table: public.actual_snap

CREATE TABLE public.actual_snap
(
    snap_id integer NOT NULL,
    group_id integer NOT NULL,
    CONSTRAINT actual_snap_group_id_pk UNIQUE (group_id)
);

-- Table: public.faculty

CREATE TABLE public.faculty
(
    faculty_desc character varying(300),
    faculty_id integer,
    faculty_act_flg character varying(1) DEFAULT 'Y'::character varying,
    CONSTRAINT faculty_faculty_id_pk UNIQUE (faculty_id)
);

-- Table: public."group"

CREATE TABLE public."group"
(
    group_id integer,
    group_name character varying(20),
    group_create_dttm date,
    group_stud_cnt double precision,
    group_active character varying(4),
    group_type character varying(20),
    group_load_flg character varying(4),
    group_faculty_id integer,
    CONSTRAINT group_group_id_pk UNIQUE (group_id)
);

-- Table: public.lecturer

CREATE TABLE public.lecturer
(
    lect_id integer NOT NULL,
    lect_fio character varying(200),
    lect_dept character varying(400),
    lect_birtday character varying(16),
    lect_email character varying(100),
    CONSTRAINT lecturer_pkey PRIMARY KEY (lect_id)
);

-- Table: public.registry_snap

CREATE TABLE public.registry_snap
(
    snap_id integer NOT NULL DEFAULT nextval('snap_id_seq'::regclass),
    snap_group_id integer NOT NULL,
    snap_dttm timestamp without time zone DEFAULT (now())::timestamp without time zone,
    CONSTRAINT registry_snap_snap_id_snap_group_id_pk PRIMARY KEY (snap_id, snap_group_id)
);

-- Table: public.schedule

CREATE TABLE public.schedule
(
    "time" character varying(120),
    groups character varying(350),
    discipline character varying(400) NOT NULL,
    tutors character varying,
    comments character varying,
    date date NOT NULL,
    group_id integer NOT NULL,
    time_id integer NOT NULL,
    week_id integer,
    snap_id integer NOT NULL,
    id_row integer NOT NULL DEFAULT nextval('schedule_id_row_seq1'::regclass),
    exam_flg character varying,
    CONSTRAINT schedule_pk PRIMARY KEY (snap_id, group_id, date, discipline, time_id, id_row)
);

-- Table: public.time_class

CREATE TABLE public.time_class
(
    time_id integer NOT NULL,
    time_number integer,
    time_start time without time zone,
    time_end time without time zone,
    time_str character varying(13),
    CONSTRAINT time_class_pkey PRIMARY KEY (time_id)
);


-- Table: public."user"

CREATE TABLE public."user"
(
    user_id character varying(20) NOT NULL,
    user_name character varying(200),
    user_group_id integer,
    user_group_name character varying(20) COLLATE pg_catalog."default",
    user_create_dttm timestamp without time zone DEFAULT now(),
    additional_group_id integer,
    CONSTRAINT user_pkey PRIMARY KEY (user_id)
);

-- Table: public.week_type

CREATE TABLE public.week_type
(
    week_id integer NOT NULL,
    week_desc character varying(20),
    CONSTRAINT week_type_pkey PRIMARY KEY (week_id)
);
