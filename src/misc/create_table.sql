CREATE TABLE asm_source(
  id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'id',
  name VARCHAR(256) COMMENT 'function name',
  x86_code TEXT COMMENT 'x86_code',
  arm_code TEXT COMMENT 'arm_code'
);

CREATE TABLE train_data(
  id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'id',
  name VARCHAR(256) COMMENT 'function name',
  x86_code TEXT COMMENT 'x86_code',
  arm_code TEXT COMMENT 'arm_code'
);

-- debian-sys-maint
-- MUYqBk5n4tgbjaeH