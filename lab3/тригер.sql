DROP TABLE IF EXISTS "reader";
CREATE TABLE "reader"(
        "readerID" bigserial PRIMARY KEY,
        "readerName" varchar(255)
);


CREATE OR REPLACE FUNCTION update_insert_func() RETURNS TRIGGER as $$
DECLARE
	curs CURSOR FOR SELECT * FROM "reader";
	m_row "reader"%ROWTYPE;
begin
	IF TG_OP = 'INSERT' then
	for m_row in curs loop
		UPDATE "reader" SET "readerName"=m_row."readerName" || 'a' WHERE current of curs;
	END LOOP;
	RAISE NOTICE 'Triggered on inserting!';
	return m_row;
	else
		RAISE NOTICE 'Triggered on updating!';
		return NULL;
	END IF;
END;

$$ LANGUAGE plpgsql;

CREATE TRIGGER "test_trigger"
AFTER UPDATE OR INSERT ON "reader"
FOR EACH ROW
EXECUTE procedure update_insert_func();

INSERT INTO "reader"("readerName")
VALUES ('reader1'), ('reader2'), ('reader3'), ('reader4'), ('reader5');

SELECT * FROM "reader";

INSERT INTO "reader"("readerName") VALUES ('reader6');
UPDATE "reader" SET "readerName" = 'READER';
DELETE FROM "reader" WHERE "readerID" = 6;