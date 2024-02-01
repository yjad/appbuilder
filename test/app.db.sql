BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "ab_permission" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(100) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("name")
);
CREATE TABLE IF NOT EXISTS "ab_view_menu" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(250) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("name")
);
CREATE TABLE IF NOT EXISTS "ab_role" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("name")
);
CREATE TABLE IF NOT EXISTS "ab_user" (
	"id"	INTEGER NOT NULL,
	"first_name"	VARCHAR(64) NOT NULL,
	"last_name"	VARCHAR(64) NOT NULL,
	"username"	VARCHAR(64) NOT NULL,
	"password"	VARCHAR(256),
	"active"	BOOLEAN,
	"email"	VARCHAR(320) NOT NULL,
	"last_login"	DATETIME,
	"login_count"	INTEGER,
	"fail_login_count"	INTEGER,
	"created_on"	DATETIME,
	"changed_on"	DATETIME,
	"created_by_fk"	INTEGER,
	"changed_by_fk"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("changed_by_fk") REFERENCES "ab_user"("id"),
	FOREIGN KEY("created_by_fk") REFERENCES "ab_user"("id"),
	UNIQUE("username"),
	UNIQUE("email")
);
CREATE TABLE IF NOT EXISTS "ab_register_user" (
	"id"	INTEGER NOT NULL,
	"first_name"	VARCHAR(64) NOT NULL,
	"last_name"	VARCHAR(64) NOT NULL,
	"username"	VARCHAR(64) NOT NULL,
	"password"	VARCHAR(256),
	"email"	VARCHAR(64) NOT NULL,
	"registration_date"	DATETIME,
	"registration_hash"	VARCHAR(256),
	PRIMARY KEY("id"),
	UNIQUE("username")
);
CREATE TABLE IF NOT EXISTS "ab_permission_view" (
	"id"	INTEGER NOT NULL,
	"permission_id"	INTEGER,
	"view_menu_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("permission_id") REFERENCES "ab_permission"("id"),
	FOREIGN KEY("view_menu_id") REFERENCES "ab_view_menu"("id"),
	UNIQUE("permission_id","view_menu_id")
);
CREATE TABLE IF NOT EXISTS "ab_user_role" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER,
	"role_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("role_id") REFERENCES "ab_role"("id"),
	FOREIGN KEY("user_id") REFERENCES "ab_user"("id"),
	UNIQUE("user_id","role_id")
);
CREATE TABLE IF NOT EXISTS "ab_permission_view_role" (
	"id"	INTEGER NOT NULL,
	"permission_view_id"	INTEGER,
	"role_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("role_id") REFERENCES "ab_role"("id"),
	FOREIGN KEY("permission_view_id") REFERENCES "ab_permission_view"("id"),
	UNIQUE("permission_view_id","role_id")
);
CREATE TABLE IF NOT EXISTS "contact_group" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("name")
);
CREATE TABLE IF NOT EXISTS "gender" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("name")
);
CREATE TABLE IF NOT EXISTS "contact" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(150) NOT NULL,
	"address"	VARCHAR(564),
	"birthday"	DATE,
	"personal_phone"	VARCHAR(20),
	"personal_celphone"	VARCHAR(20),
	"contact_group_id"	INTEGER NOT NULL,
	"gender_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("contact_group_id") REFERENCES "contact_group"("id"),
	FOREIGN KEY("gender_id") REFERENCES "gender"("id"),
	UNIQUE("name")
);
CREATE TABLE IF NOT EXISTS "status" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("name")
);
CREATE TABLE IF NOT EXISTS "semester" (
	"id"	INTEGER NOT NULL,
	"semester_no"	CHAR(5) NOT NULL,
	"description"	VARCHAR(20) NOT NULL,
	"book_start_date"	DATE NOT NULL,
	"exam_start_date"	DATE,
	"exam_end_date"	DATE,
	"status_id"	INTEGER NOT NULL,
	"create_date"	DATE NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("status_id") REFERENCES "status"("id"),
	UNIQUE("semester_no"),
	UNIQUE("id")
);
CREATE TABLE IF NOT EXISTS "trx_code" (
	"trx_code"	INTEGER NOT NULL,
	"description"	VARCHAR(40),
	"db_cr"	CHAR(2),
	PRIMARY KEY("trx_code")
);
CREATE TABLE IF NOT EXISTS "level" (
	"id"	CHAR(2) NOT NULL UNIQUE,
	"level"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("level")
);
CREATE TABLE IF NOT EXISTS "teller" (
	"trx_id"	INTEGER NOT NULL UNIQUE,
	"user_id"	VARCHAR(20),
	"trx_date"	DATETIME NOT NULL,
	"amount"	NUMERIC,
	"db_cr"	CHAR(2),
	"trx_code"	INTEGER NOT NULL,
	"description"	VARCHAR(40),
	"reversed"	CHAR(1),
	"reverse_date"	DATETIME,
	"student_id"	INTEGER NOT NULL,
	"level_id"	CHAR(2),
	"semester_no"	CHAR(5),
	"payee"	VARCHAR(20),
	PRIMARY KEY("trx_id" AUTOINCREMENT),
	FOREIGN KEY("student_id") REFERENCES "student"("id"),
	FOREIGN KEY("level_id") REFERENCES "level"("id"),
	FOREIGN KEY("semester_no") REFERENCES "semester"("id"),
	FOREIGN KEY("trx_code") REFERENCES "trx_code"("trx_code")
);
CREATE TABLE IF NOT EXISTS "student_level" (
	"student_id"	INTEGER NOT NULL,
	"level_id"	CHAR(2) NOT NULL,
	"comment"	VARCHAR(40),
	"user_id"	INTEGER NOT NULL,
	"create_date"	DATE NOT NULL,
	PRIMARY KEY("student_id","level_id"),
	FOREIGN KEY("student_id") REFERENCES "student"("id"),
	FOREIGN KEY("user_id") REFERENCES "ab_user"("id"),
	FOREIGN KEY("level_id") REFERENCES "level"("id")
);
CREATE TABLE IF NOT EXISTS "country" (
	"id"	INTEGER NOT NULL,
	"country"	VARCHAR(20),
	"alpha_2_code"	VARCHAR(2),
	"alpha_3_code"	VARCHAR(4) NOT NULL,
	"un_code"	VARCHAR(3),
	"country_ar"	VARCHAR(20),
	PRIMARY KEY("alpha_3_code")
);
CREATE TABLE IF NOT EXISTS "student_semester" (
	"student_id"	INTEGER NOT NULL,
	"level_id"	INTEGER NOT NULL,
	"semester_id"	CHAR(5) NOT NULL,
	"comment"	VARCHAR(40),
	"user_id"	INTEGER,
	"create_date"	DATE NOT NULL,
	PRIMARY KEY("student_id","level_id","semester_id"),
	FOREIGN KEY("level_id") REFERENCES "student_level"("level_id"),
	FOREIGN KEY("student_id") REFERENCES "student"("id"),
	FOREIGN KEY("user_id") REFERENCES "ab_user"("id"),
	FOREIGN KEY("semester_id") REFERENCES "semester"("id"),
	UNIQUE("semester_id")
);
CREATE TABLE IF NOT EXISTS "student" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(20) NOT NULL,
	"name_en"	VARCHAR(20) NOT NULL,
	"passport_no"	VARCHAR(20) NOT NULL,
	"birth_dt"	DATETIME,
	"nationality_id"	CHAR(3) NOT NULL,
	"gender_id"	INTEGER NOT NULL,
	"phone_no"	VARCHAR(20) NOT NULL,
	"whats_up"	VARCHAR(20) NOT NULL,
	"address"	VARCHAR(200) NOT NULL,
	"district"	VARCHAR(20) NOT NULL,
	"street_name"	VARCHAR(20) NOT NULL,
	"building_no"	VARCHAR(20) NOT NULL,
	"ref_name"	VARCHAR(20) NOT NULL,
	"ref_address"	VARCHAR(20) NOT NULL,
	"how_did_know"	VARCHAR(20) NOT NULL,
	"level_id"	CHAR(2),
	"semester_id"	INTEGER,
	"status_id"	INTEGER NOT NULL,
	"add_dt"	DATETIME NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("nationality_id") REFERENCES "country"("alpha_3_code"),
	FOREIGN KEY("gender_id") REFERENCES "gender"("id"),
	FOREIGN KEY("status_id") REFERENCES "status"("id")
);
COMMIT;
