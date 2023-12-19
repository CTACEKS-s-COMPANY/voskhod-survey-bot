-- -------------------------------------------------------------
-- Database: postgres
-- Generation Time: 2023-12-19 22:28:34.0080
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS answers_id_seq;

-- Table Definition
CREATE TABLE "public"."answers" (
    "id" int4 NOT NULL DEFAULT nextval('answers_id_seq'::regclass),
    "date_creation" timestamp NOT NULL default current_timestamp,
    "user_id" int4 NOT NULL,
    "post_id" int4,
    "isAnsw" bool DEFAULT false,
    "description" varchar(255) NOT NULL,
    PRIMARY KEY ("id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS posts_id_seq;

-- Table Definition
CREATE TABLE "public"."posts" (
    "id" int4 NOT NULL DEFAULT nextval('posts_id_seq'::regclass),
    "author_id" int4,
    "text" varchar(255) NOT NULL,
    "date_creation" timestamp NOT NULL default current_timestamp,
    PRIMARY KEY ("id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."users" (
    "id" int4 NOT NULL,
    "is_subscriber" bool NOT NULL DEFAULT false,
    "is_admin" bool NOT NULL DEFAULT false,
    "date_creation" timestamp NOT NULL default current_timestamp,
    PRIMARY KEY ("id")
);

ALTER TABLE "public"."answers" ADD FOREIGN KEY ("user_id") REFERENCES "public"."users"("id");
ALTER TABLE "public"."answers" ADD FOREIGN KEY ("post_id") REFERENCES "public"."posts"("id");
ALTER TABLE "public"."posts" ADD FOREIGN KEY ("author_id") REFERENCES "public"."users"("id");
