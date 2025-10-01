from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            username VARCHAR(255) NULL,
            phone VARCHAR(55),
            score INT DEFAULT 0,
            oldd VARCHAR(3),
            telegram_id BIGINT NOT NULL UNIQUE,
            user_args VARCHAR(55) NULL,
            status VARCHAR(255) NOT NULL DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON Users(telegram_id);
        CREATE INDEX IF NOT EXISTS idx_users_score ON Users(score);
        """
        await self.execute(sql, execute=True)
        
    async def create_table_user_number(self):
        sql = """
        CREATE TABLE IF NOT EXISTS user_number (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT
        );
        """
        await self.execute(sql, execute=True)

    # async def create_table_winner_users(self):
    #     sql = """
    #     CREATE TABLE IF NOT EXISTS winner_users (
    #         id SERIAL PRIMARY KEY,
    #         full_name VARCHAR(255) NOT NULL,
    #         username VARCHAR(255) NULL,
    #         telegram_id BIGINT NOT NULL UNIQUE,
    #         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #     );
    #     """
    #     await self.execute(sql, execute=True)

    async def create_table_one_time_link(self):
        sql = """
        CREATE TABLE IF NOT EXISTS one_time_link (
        id SERIAL PRIMARY KEY,
        full_name varchar(125) NULL,
        username varchar(125) NULL,
        link varchar(55),
        telegram_id BIGINT DEFAULT 111,
        private_channel_id VARCHAR(55)
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_add_list(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Add_List (
        id SERIAL PRIMARY KEY,
        url varchar(301) NOT NULL,
        button_name varchar(301) NOT NULL
                        );
        """
        await self.execute(sql, execute=True)


    async def create_table_tugma(self):
        sql = """
        CREATE TABLE IF NOT EXISTS tugma (
        id SERIAL PRIMARY KEY,
        link varchar(301) NOT NULL,
        link_name TEXT NULL,
        order_button INTEGER NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_requested_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS requested_users (
        id SERIAL PRIMARY KEY,
        url_1 varchar(11),
        url_2 varchar(11),
        url_3 varchar(11),
        url_4 varchar(11),
        url_5 varchar(11),
        url_6 varchar(11),
        url_7 varchar(11),
        url_8 varchar(11),
        url_9 varchar(11),
        telegram_id BIGINT NOT NULL UNIQUE
                );
        CREATE INDEX IF NOT EXISTS idx_requested_users_telegram_id ON requested_users(telegram_id);
        """
        await self.execute(sql, execute=True)

    async def create_table_chanel(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Channel (
        id SERIAL PRIMARY KEY,
        chanelll VARCHAR(301) NOT NULL,
        url varchar(301) NOT NULL,
        channel_name TEXT NULL,
        order_button INTEGER NULL
                );
        CREATE INDEX IF NOT EXISTS idx_channel_chanelll ON Channel(chanelll);
        """
        await self.execute(sql, execute=True)

    async def create_table_add_list_chanel(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Add_List_Channel (
        id SERIAL PRIMARY KEY,
        url varchar(301) NOT NULL,
        order_button INTEGER NULL
                        );
        """
        await self.execute(sql, execute=True)
    async def create_table_request_join_chanel(self):
        sql = """
        CREATE TABLE IF NOT EXISTS request_join_chanel (
        id SERIAL PRIMARY KEY,
        channel_id VARCHAR(301) NOT NULL,
        url varchar(301) NOT NULL,
        channel_name TEXT NULL,
        order_button INTEGER NULL
                );
        """
        await self.execute(sql, execute=True)

    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS admins (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL UNIQUE
                );
        """
        await self.execute(sql, execute=True)

    async def create_table_chanel_element(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Elementt (
        id SERIAL PRIMARY KEY,
        photo TEXT NULL,
        channel_id TEXT NULL,
        main_req_text TEXT DEFAULT '<b>🚀 Loyihada </b> ishtirok etish uchun quyidagi kanallarga aʼzo boʼling!\n\n<i>⚠️ Yopiq kanallarga ulanish soʼrovini yuborishingiz kifoya.</i>\nKeyin <b>✅ A’zo boʼldim</b> tugmasini bosing',
        game_text TEXT NULL,
        shartlar TEXT NULL,
        limit_score INT DEFAULT 1,
        limit_require INT DEFAULT 5,
        winners INT DEFAULT 20,
        bot_url varchar(255)
                );
        """
        await self.execute(sql, execute=True)

    async def create_table_buttons(self):
        sql = """
        CREATE TABLE IF NOT EXISTS buttons (
        id SERIAL PRIMARY KEY,
        button_name VARCHAR(301) NOT NULL
                );
        """
        await self.execute(sql, execute=True)

    async def create_table_lessons(self):
        sql = """
        CREATE TABLE IF NOT EXISTS lessons (
            id SERIAL PRIMARY KEY,
            button_name VARCHAR(301) NOT NULL,
            type VARCHAR(301) NOT NULL,
            file_id VARCHAR(301) NULL,
            file_unique_id VARCHAR(301) NOT NULL,
            description TEXT NULL,
            is_link BOOLEAN DEFAULT FALSE,
            score INTEGER NULL,
            private_channel_id VARCHAR(55) NULL
        );

        CREATE INDEX IF NOT EXISTS idx_lessons_button ON lessons(button_name);
        CREATE INDEX IF NOT EXISTS idx_lessons_is_link ON lessons(is_link);
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, telegram_id, username, phone, oldd, user_args):
        sql = "INSERT INTO users (full_name, telegram_id, username, phone, oldd, user_args) VALUES($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, full_name, telegram_id, username, phone, oldd, user_args, fetchrow=True)

    async def add_userrr(self, full_name, telegram_id, username, phone, score):
        sql = "INSERT INTO users (full_name, telegram_id, username, phone, score) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, full_name, telegram_id, username, phone, score, fetchrow=True)

    async def add_userr(self, full_name, telegram_id, username, score):
        sql = "INSERT INTO users (full_name, telegram_id, username, score) VALUES($1, $2, $3,$4) returning *"
        return await self.execute(sql, full_name, telegram_id, username, score, fetchrow=True)

    async def add_lesson_text(self, button_name, type, file_unique_id, description, score=None, is_link=None, private_channel_id=None):
        sql = "INSERT INTO lessons (button_name,type,file_unique_id,description,score,is_link,private_channel_id) VALUES($1,$2,$3,$4,$5,$6,$7) returning *"
        return await self.execute(sql, button_name, type, file_unique_id, description, score, is_link,
                                  private_channel_id, fetchrow=True)

    async def add_json_file_user(self, full_name, username, phone, telegram_id, score):
        sql = "INSERT INTO users (full_name, username, phone, telegram_id, score) VALUES($1, $2, $3,$4,$5) returning *"
        return await self.execute(sql, full_name, username, phone, telegram_id, score, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_all_active_users(self):
        sql = "SELECT telegram_id FROM Users where status='active'"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_top_users(self, lim_win):
        sql = f"SELECT * FROM Users WHERE score IS NOT NULL ORDER BY score DESC LIMIT {lim_win}"
        return await self.execute(sql, fetch=True)

    async def select_top_users_list(self):
        sql = f"SELECT * FROM Users WHERE score IS NOT NULL ORDER BY score DESC"
        return await self.execute(sql, fetch=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def count_active_users(self):
        sql = "SELECT COUNT(*) FROM Users where status='active'"
        return await self.execute(sql, fetchval=True)

    async def count_block_users(self):
        sql = "SELECT COUNT(*) FROM Users where status='block'"
        return await self.execute(sql, fetchval=True)

    async def update_user_name(self, name, telegram_id):
        sql = "UPDATE Users SET full_name=$1 WHERE telegram_id=$2"
        return await self.execute(sql, name, telegram_id, execute=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_user_oldd(self, oldd, telegram_id):
        sql = "UPDATE Users SET oldd=$1 WHERE telegram_id=$2"
        return await self.execute(sql, oldd, telegram_id, execute=True)

    async def update_user_args(self, user_args, telegram_id):
        sql = "UPDATE Users SET user_args=$1 WHERE telegram_id=$2"
        return await self.execute(sql, user_args, telegram_id, execute=True)

    async def update_user_phone(self, phone, telegram_id):
        sql = "UPDATE Users SET phone=$1 WHERE telegram_id=$2"
        return await self.execute(sql, phone, telegram_id, execute=True)

    async def update_user_status(self, status, telegram_id):
        sql = "UPDATE Users SET status=$1 WHERE telegram_id=$2"
        return await self.execute(sql, status, telegram_id, execute=True)

    async def update_user_score(self, score, telegram_id):
        sql = "UPDATE Users SET score=$1 WHERE telegram_id=$2"
        return await self.execute(sql, score, telegram_id, execute=True)

    async def update_users_all_score(self):
        sql = "UPDATE Users SET score=0"
        return await self.execute(sql, execute=True)

    async def update_users_all_args(self):
        sql = "UPDATE Users SET phone='---', oldd='new', user_args='---'"
        return await self.execute(sql, execute=True)

    async def delete_users(self, telegram_id):
        sql = "DELETE FROM Users WHERE telegram_id=$1"
        await self.execute(sql, telegram_id, execute=True)

    async def delete_admin(self, admin_id):
        sql = "DELETE FROM admins WHERE admin_id=$1"
        await self.execute(sql, admin_id, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def delete_channel(self, chanel):
        sql = "DELETE FROM Channel WHERE chanelll=$1"
        await self.execute(sql, chanel, execute=True)


    async def add_chanell(self, chanelll, url, channel_name, order_button):
        sql = "INSERT INTO Channel (chanelll, url,channel_name, order_button) VALUES($1, $2,$3,$4) returning *"
        return await self.execute(sql, chanelll, url, channel_name, order_button, fetchrow=True)

    async def get_chanel(self, channel):
        sql = f"SELECT * FROM Channel WHERE chanelll=$1"
        return await self.execute(sql, channel, fetch=True)

    async def get_admins(self):
        sql = f"SELECT * FROM admins"
        return await self.execute(sql, fetch=True)

    async def drop_Chanel(self):
        await self.execute("DROP TABLE Channel", execute=True)

    async def select_chanel(self):
        sql = "SELECT * FROM Channel"
        return await self.execute(sql, fetch=True)

    async def add_photo(self, photo):
        sql = "INSERT INTO Elementt (photo) VALUES($1) returning *"
        return await self.execute(sql, photo, fetchrow=True)

    async def add_channel_id(self, channel_id):
        sql = "INSERT INTO Elementt (channel_id) VALUES($1) returning *"
        return await self.execute(sql, channel_id, fetchrow=True)

    async def add_main_req_text(self, main_req_text):
        sql = "INSERT INTO Elementt (main_req_text) VALUES($1) returning *"
        return await self.execute(sql, main_req_text, fetchrow=True)

    async def add_shartlar(self, shartlar):
        sql = "INSERT INTO Elementt (shartlar) VALUES($1) returning *"
        return await self.execute(sql, shartlar, fetchrow=True)

    async def add_text(self, bot_url):
        sql = "INSERT INTO Elementt (bot_url) VALUES($1) returning *"
        return await self.execute(sql, bot_url, fetchrow=True)

    async def add_bot_url(self, bot_url):
        sql = "INSERT INTO Elementt (bot_url) VALUES($1) returning *"
        return await self.execute(sql, bot_url, fetchrow=True)

    async def update_photo(self, photo):
        sql = "UPDATE Elementt SET photo=$1 WHERE id=1"
        return await self.execute(sql, photo, execute=True)

    async def update_limit_score(self, limit_score):
        sql = "UPDATE Elementt SET limit_score=$1 WHERE id=1"
        return await self.execute(sql, limit_score, execute=True)
    
    async def update_all_users_data(self, args, oldd):
        sql = "UPDATE Users SET user_args=$1, oldd=$2, score=0"
        return await self.execute(sql, args, oldd, execute=True)

    async def add_limit_require(self, limit_score):
        sql = "INSERT INTO Elementt (limit_score) VALUES($1) returning *"
        return await self.execute(sql, limit_score, fetchrow=True)

    async def update_limit_require(self, limit_require):
        sql = "UPDATE Elementt SET limit_require=$1 WHERE id=1"
        return await self.execute(sql, limit_require, execute=True)

    async def winners(self, winners):
        sql = "UPDATE Elementt SET winners=$1 WHERE id=1"
        return await self.execute(sql, winners, execute=True)

    async def update_game_text(self, game_text):
        sql = "UPDATE Elementt SET game_text=$1 WHERE id=1"
        return await self.execute(sql, game_text, execute=True)

    async def bot_url(self, bot_url):
        sql = "UPDATE Elementt SET bot_url=$1 WHERE id=1"
        return await self.execute(sql, bot_url, execute=True)

    async def update_channel_id(self, channel_id):
        sql = "UPDATE Elementt SET channel_id=$1 WHERE id=1"
        return await self.execute(sql, channel_id, execute=True)

    async def update_main_req_text(self, main_req_text):
        sql = "UPDATE Elementt SET main_req_text=$1 WHERE id=1"
        return await self.execute(sql, main_req_text, execute=True)

    async def update_shartlar(self, shartlar):
        sql = "UPDATE Elementt SET shartlar=$1 WHERE id=1"
        return await self.execute(sql, shartlar, execute=True)

    async def get_elements(self):
        sql = f"SELECT * FROM Elementt WHERE id=1"
        return await self.execute(sql, fetch=True)

    async def drop_elements(self):
        await self.execute("DROP TABLE Elementt", execute=True)

    async def drop_lessons(self):
        await self.execute("DROP TABLE lessons", execute=True)

    ### Lessons DB Commands
    async def add_button(self, button_name):
        sql = "INSERT INTO buttons (button_name) VALUES($1) returning *"
        return await self.execute(sql, button_name, fetchrow=True)

    async def delete_button_name(self, button_name):
        sql = "DELETE FROM buttons WHERE button_name=$1"
        await self.execute(sql, button_name, execute=True)

    async def select_buttons(self):
        sql = "SELECT * FROM buttons"
        return await self.execute(sql, fetch=True)

    async def add_lesson(self, button_name, type, file_id, file_unique_id, score=None, is_link=False, private_channel_id='',
                         description=None):
        sql = "INSERT INTO lessons (button_name,type,file_id,file_unique_id, score, is_link, private_channel_id,description) VALUES($1,$2,$3,$4,$5,$6,$7,$8) returning *"
        return await self.execute(sql, button_name, type, file_id, file_unique_id, score, is_link,
                                  private_channel_id, description, fetchrow=True)

    async def delete_lesson(self, id):
        sql = "DELETE FROM lessons WHERE id=$1"
        await self.execute(sql, id, execute=True)

    async def delete_related_lesson(self, button_name):
        sql = "DELETE FROM lessons WHERE button_name=$1"
        await self.execute(sql, button_name, execute=True)

    async def select_lessons(self):
        sql = "SELECT * FROM lessons"
        return await self.execute(sql, fetch=True)

    async def select_related_lessons(self, button_name):
        sql = "SELECT * FROM lessons WHERE button_name=$1"
        return await self.execute(sql, button_name, fetch=True)

    async def select_for_winner_gifts(self, button_name, score):
        sql = "SELECT * FROM lessons WHERE button_name=$1 and score=$2"
        return await self.execute(sql, button_name, score, fetch=True)

    ##### Admin #####
    async def add_admin(self, telegram_id):
        sql = "INSERT INTO admins (telegram_id) VALUES($1) returning *"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def select_all_admins(self):
        sql = "SELECT * FROM admins"
        return await self.execute(sql, fetch=True)

    async def delete_admins(self, telegram_id):
        sql = "DELETE FROM admins WHERE telegram_id=$1"
        await self.execute(sql, telegram_id, execute=True)

    async def drop_admins(self):
        await self.execute("DROP TABLE admins", execute=True)

    # for requested channel

    async def add_requested_users(self, telegram_id):
        sql = "INSERT INTO requested_users (telegram_id) VALUES($1) returning *"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def get_requested_users(self, telegram_id):
        sql = f"SELECT * FROM requested_users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetch=True)

    async def update_url_1(self, url_1, telegram_id):
        sql = "UPDATE requested_users SET url_1=$1 WHERE telegram_id=$2"
        return await self.execute(sql, url_1, telegram_id, execute=True)

    async def update_url_2(self, url_2, telegram_id):
        sql = "UPDATE requested_users SET url_2=$1 WHERE telegram_id=$2"
        return await self.execute(sql, url_2, telegram_id, execute=True)

    async def update_url_3(self, url_3, telegram_id):
        sql = "UPDATE requested_users SET url_3=$1 WHERE telegram_id=$2"
        return await self.execute(sql, url_3, telegram_id, execute=True)

    async def update_url_4(self, url_4, telegram_id):
        sql = "UPDATE requested_users SET url_4=$1 WHERE telegram_id=$2"
        return await self.execute(sql, url_4, telegram_id, execute=True)

    async def update_url_5(self, url_5, telegram_id):
        sql = "UPDATE requested_users SET url_5=$1 WHERE telegram_id=$2"
        return await self.execute(sql, url_5, telegram_id, execute=True)

    async def update_url_6(self, url_6, telegram_id):
        sql = "UPDATE requested_users SET url_6=$1 WHERE telegram_id=$2"
        return await self.execute(sql, url_6, telegram_id, execute=True)

    async def update_url_7(self, url_7, telegram_id):
        sql = "UPDATE requested_users SET url_7=$1 WHERE telegram_id=$2"
        return await self.execute(sql, url_7, telegram_id, execute=True)

    async def update_url_8(self, url_8, telegram_id):
        sql = "UPDATE requested_users SET url_8=$1 WHERE telegram_id=$2"
        return await self.execute(sql, url_8, telegram_id, execute=True)

    async def update_url_9(self, url_9, telegram_id):
        sql = "UPDATE requested_users SET url_9=$1 WHERE telegram_id=$2"
        return await self.execute(sql, url_9, telegram_id, execute=True)

    async def drop_requested_users(self):
        await self.execute("DROP TABLE requested_users", execute=True)

    # Join Request Channel DB codes
    async def select_req_j_chanel(self):
        sql = "SELECT * FROM request_join_chanel"
        return await self.execute(sql, fetch=True)

    async def add_req_j_channel(self, channel_id, url, channel_name, order_button):
        sql = "INSERT INTO request_join_chanel (channel_id, url,channel_name, order_button) VALUES($1, $2,$3,$4) returning *"
        return await self.execute(sql, channel_id, url, channel_name, order_button, fetchrow=True)

    async def get_req_j_chanel(self, channel_id):
        sql = f"SELECT * FROM request_join_chanel WHERE channel_id=$1"
        return await self.execute(sql, channel_id, fetch=True)

    async def drop_req_j_Chanel(self):
        await self.execute("DROP TABLE request_join_chanel", execute=True)

    async def delete_req_j_channel(self, channel_id):
        sql = "DELETE FROM request_join_chanel WHERE channel_id=$1"
        await self.execute(sql, channel_id, execute=True)

    async def select_tugma(self):
        sql = "SELECT * FROM tugma"
        return await self.execute(sql, fetch=True)

    async def add_tugma(self, link, link_name, order_button):
        sql = "INSERT INTO tugma (link,link_name, order_button) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, link, link_name, order_button, fetchrow=True)

    async def get_tugma(self, link):
        sql = f"SELECT * FROM tugma WHERE link=$1"
        return await self.execute(sql, link, fetch=True)

    async def drop_tugma(self):
        await self.execute("DROP TABLE tugma", execute=True)

    async def delete_tugma(self, link):
        sql = "DELETE FROM tugma WHERE link=$1"
        await self.execute(sql, link, execute=True)

    # Add list
    async def add_channel_for_add_list(self, url):
        sql = "INSERT INTO Add_List_Channel (url) VALUES($1) returning *"
        return await self.execute(sql, url, fetchrow=True)

    async def get_add_list_chanel(self, url):
        sql = f"SELECT * FROM Add_List_Channel WHERE url=$1"
        return await self.execute(sql, url, fetch=True)

    async def delete_add_list_channel(self, url):
        sql = "DELETE FROM Add_List_Channel WHERE url=$1"
        await self.execute(sql, url, execute=True)

    async def add_add_list(self, url, button_name):
        sql = "INSERT INTO Add_List (url, button_name) VALUES($1,$2) returning *"
        return await self.execute(sql, url, button_name, fetchrow=True)

    async def delete_add_list(self, url):
        sql = "DELETE FROM Add_List WHERE url=$1"
        await self.execute(sql, url, execute=True)

    async def select_chanel_add_list(self):
        sql = "SELECT * FROM Add_List_Channel"
        return await self.execute(sql, fetch=True)

    async def select_add_list(self):
        sql = "SELECT * FROM Add_List"
        return await self.execute(sql, fetch=True)

    async def select_add_list_channels(self):
        sql = "SELECT * FROM Add_List_Channel"
        return await self.execute(sql, fetch=True)

    async def add_one_time_link(self, link, private_channel_id):
        sql = "INSERT INTO one_time_link (link,private_channel_id) VALUES($1,$2) returning *"
        return await self.execute(sql, link, private_channel_id, fetchrow=True)

    async def select_one_time_all_links(self, private_channel_id):
        sql = "SELECT COUNT(*) FROM one_time_link WHERE private_channel_id=$1 and telegram_id=111;"
        return await self.execute(sql, private_channel_id, fetchval=True)
    
    async def select_one_time_link(self, private_channel_id):
        sql = "SELECT * FROM one_time_link WHERE private_channel_id=$1 and telegram_id=111 LIMIT 1;"
        return await self.execute(sql, private_channel_id, fetch=True)

    async def update_one_time_link_column(self, telegram_id, link):
        sql = "UPDATE one_time_link SET telegram_id=$1 WHERE link=$2"
        return await self.execute(sql, telegram_id, link, execute=True)
    async def add_user_number(self, full_name, username, telegram_id):
        sql = "INSERT INTO user_number (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_user_number(self, **kwargs):
        sql = "SELECT * FROM user_number WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def drop_users_number(self):
        await self.execute("DROP TABLE user_number", execute=True)

    async def select_all_user_number(self):
        sql = "SELECT * FROM user_number"
        return await self.execute(sql, fetch=True)

    async def count_users_number(self):
        sql = "SELECT COUNT(*) FROM user_number"
        return await self.execute(sql, fetchval=True)

    # Test System Database Methods
    async def create_table_tests(self):
        sql = """
        CREATE TABLE IF NOT EXISTS tests (
            id SERIAL PRIMARY KEY,
            test_code VARCHAR(50) NOT NULL UNIQUE,
            test_name VARCHAR(255) NOT NULL,
            description TEXT,
            total_questions INTEGER NOT NULL,
            correct_answers TEXT NOT NULL,
            time_limit INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            created_by BIGINT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_tests_code ON tests(test_code);
        CREATE INDEX IF NOT EXISTS idx_tests_active ON tests(is_active);
        """
        await self.execute(sql, execute=True)

    async def create_table_test_attempts(self):
        sql = """
        CREATE TABLE IF NOT EXISTS test_attempts (
            id SERIAL PRIMARY KEY,
            test_id INTEGER NOT NULL REFERENCES tests(id) ON DELETE CASCADE,
            user_id BIGINT NOT NULL,
            user_answers TEXT NOT NULL,
            score INTEGER DEFAULT 0,
            total_questions INTEGER NOT NULL,
            correct_answers INTEGER DEFAULT 0,
            percentage DECIMAL(5,2) DEFAULT 0.00,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(test_id, user_id)
        );
        
        CREATE INDEX IF NOT EXISTS idx_test_attempts_test_id ON test_attempts(test_id);
        CREATE INDEX IF NOT EXISTS idx_test_attempts_user_id ON test_attempts(user_id);
        CREATE INDEX IF NOT EXISTS idx_test_attempts_score ON test_attempts(score);
        """
        await self.execute(sql, execute=True)

    # Test Management Methods
    async def add_test(self, test_code, test_name, description, total_questions, correct_answers, time_limit, created_by):
        sql = """
        INSERT INTO tests (test_code, test_name, description, total_questions, correct_answers, time_limit, created_by) 
        VALUES($1, $2, $3, $4, $5, $6, $7) 
        RETURNING *
        """
        return await self.execute(sql, test_code, test_name, description, total_questions, correct_answers, time_limit, created_by, fetchrow=True)

    async def get_test_by_code(self, test_code):
        sql = "SELECT * FROM tests WHERE test_code=$1"
        return await self.execute(sql, test_code, fetchrow=True)

    async def get_all_tests(self):
        sql = "SELECT * FROM tests ORDER BY created_at DESC"
        return await self.execute(sql, fetch=True)

    async def get_test_by_id(self, test_id):
        sql = "SELECT * FROM tests WHERE id=$1"
        return await self.execute(sql, test_id, fetchrow=True)

    async def update_test(self, test_id, test_name, description, total_questions, correct_answers, time_limit):
        sql = """
        UPDATE tests 
        SET test_name=$2, description=$3, total_questions=$4, correct_answers=$5, time_limit=$6 
        WHERE id=$1
        """
        return await self.execute(sql, test_id, test_name, description, total_questions, correct_answers, time_limit, execute=True)

    async def delete_test(self, test_id):
        sql = "DELETE FROM tests WHERE id=$1"
        return await self.execute(sql, test_id, execute=True)

    async def add_test_attempt(self, test_id, user_id, user_answers, score, total_questions, correct_answers, percentage):
        sql = """
        INSERT INTO test_attempts (test_id, user_id, user_answers, score, total_questions, correct_answers, percentage) 
        VALUES($1, $2, $3, $4, $5, $6, $7) 
        ON CONFLICT (test_id, user_id) 
        DO UPDATE SET 
            user_answers=EXCLUDED.user_answers,
            score=EXCLUDED.score,
            correct_answers=EXCLUDED.correct_answers,
            percentage=EXCLUDED.percentage,
            completed_at=CURRENT_TIMESTAMP
        RETURNING *
        """
        return await self.execute(sql, test_id, user_id, user_answers, score, total_questions, correct_answers, percentage, fetchrow=True)

    async def get_user_test_attempt(self, test_id, user_id):
        sql = "SELECT * FROM test_attempts WHERE test_id=$1 AND user_id=$2"
        return await self.execute(sql, test_id, user_id, fetchrow=True)

    async def get_test_attempts_by_test(self, test_id):
        sql = """
        SELECT ta.*, u.full_name, u.username 
        FROM test_attempts ta 
        JOIN users u ON ta.user_id = u.telegram_id 
        WHERE ta.test_id=$1 
        ORDER BY ta.score DESC, ta.completed_at DESC
        """
        return await self.execute(sql, test_id, fetch=True)

    async def get_user_test_history(self, user_id):
        sql = """
        SELECT ta.*, t.test_name, t.test_code 
        FROM test_attempts ta 
        JOIN tests t ON ta.test_id = t.id 
        WHERE ta.user_id=$1 
        ORDER BY ta.completed_at DESC
        """
        return await self.execute(sql, user_id, fetch=True)

    async def get_test_statistics(self, test_id):
        sql = """
        SELECT 
            COUNT(*) as total_attempts,
            AVG(percentage) as average_score,
            MAX(percentage) as highest_score,
            MIN(percentage) as lowest_score
        FROM test_attempts 
        WHERE test_id=$1
        """
        return await self.execute(sql, test_id, fetchrow=True)
