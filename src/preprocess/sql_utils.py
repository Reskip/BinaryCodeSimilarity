import pymysql

class SQL(object):
    host = "localhost"
    username = "debian-sys-maint"
    passwd = "MUYqBk5n4tgbjaeH"
    db = "mysql"

    def __init__(self):
        self._connect = pymysql.connect(
            self.host,
            self.username,
            self.passwd,
            self.db
        )
        self._cache = 0

    def insert_origin(self, name, x86_code, arm_code):
        sql = '''
        INSERT INTO
            asm_source(
                name,
                x86_code,
                arm_code
            )
        VALUES
            (
                '%s','%s','%s'
            )
        ''' % (name, x86_code, arm_code)
        cursor = self._connect.cursor()
        cursor.execute(sql)
        self.commit()

    def fetch_origin(self, num, offset):
        sql = '''
        SELECT
            *
        FROM
            asm_source
        WHERE
            id > %d
        ORDER BY
            id
        LIMIT
            %d
        ''' % (offset, num)
        cursor = self._connect.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def insert_train(self, name, x86_code, arm_code):
        sql = '''
        INSERT INTO
            train_data(
                name,
                x86_code,
                arm_code
            )
        VALUES
            (
                '%s','%s','%s'
            )
        ''' % (name, x86_code, arm_code)
        cursor = self._connect.cursor()
        cursor.execute(sql)
        self.commit()

    def fetch_train(self, num, offset):
        sql = '''
        SELECT
            *
        FROM
            train_data
        WHERE
            id > %d
        ORDER BY
            id
        LIMIT
            %d
        ''' % (offset, num)
        cursor = self._connect.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def get_source_num(self):
        sql = '''
        SELECT
            COUNT(*)
        FROM
            asm_source
        '''
        cursor = self._connect.cursor()
        cursor.execute(sql)
        return int(cursor.fetchall()[0][0])

    def get_train_num(self):
        sql = '''
        SELECT
            COUNT(*)
        FROM
            train_data
        '''
        cursor = self._connect.cursor()
        cursor.execute(sql)
        return int(cursor.fetchall()[0][0])

    def commit(self):
        if self._cache < 50:
            self._cache += 1
            return
        self._connect.commit()
        self._connect.close()
        self.__init__()

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(SQL, "_instance"):
            SQL._instance = SQL(*args, **kwargs)
        return SQL._instance