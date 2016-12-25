CREATE TABLE pending (
  id varchar(200) CONSTRAINT pending_id PRIMARY KEY  -- From the docs, it is guaranteed to not exceed 200 characters
);

CREATE TABLE new_labels (
  id varchar(200),
  x float,
  y float,
  width float,
  height float
);

CREATE TABLE labels (
  id varchar(200),
  x float,
  y float,
  width float,
  height float
);
