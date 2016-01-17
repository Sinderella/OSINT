CREATE TABLE documents (
  did INTEGER PRIMARY KEY autoincrement NOT NULL,
  url text,
  path text
);

CREATE TABLE entities (
  eid INTEGER PRIMARY KEY autoincrement NOT NULL,
  did INTEGER,
  type text,
  entity text,
  FOREIGN KEY(did) REFERENCES documents(did),
  FOREIGN KEY(type) REFERENCES entity_type(type)
);

CREATE TABLE entity_types (
  type text
);