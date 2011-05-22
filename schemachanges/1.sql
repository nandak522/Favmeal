CREATE TABLE schema_tracking (
  id serial NOT NULL,
  change varchar(6) NOT NULL,
  applied_on timestamptz NOT NULL,
  CONSTRAINT schema_tracking_pkey PRIMARY KEY (id)
);
