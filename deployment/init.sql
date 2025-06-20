CREATE TABLE ionorun (
  run_id          SERIAL       PRIMARY KEY,
  frequency_json  DOUBLE PRECISION NOT NULL,
  s0_json         JSONB        NOT NULL,
  s1_json         JSONB        NOT NULL,
  s2_json         JSONB        NOT NULL,
  s3_json         JSONB        NOT NULL,
  n0              DOUBLE PRECISION NOT NULL,
  scale_height    DOUBLE PRECISION NOT NULL,
  collision       DOUBLE PRECISION NOT NULL
);
