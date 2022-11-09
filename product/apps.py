from django.apps import AppConfig
import pymysql

class ProductConfig(AppConfig):
    name = 'product'
    def ready(self):
        print('>>>>>>>>>>>ThisisProductConfig READY!')
        with pymysql.connect(host = "mysql_container", user = "mobo", password = "mobo") as connect:
            cursor = connect.cursor()
            create_member = f"create table {name}_member( \
                              id INT,                     \
                              uid VARCHAR(32),            \
                              nickname VARCHAR(32),       \
                              email VARCHAR(254),         \
                              password VARCHAR(50),       \
                              phone VARCHAR(16),          \
                              joindate DATE,              \
                              inactive INT)"

            create_subscript = f"create table {name}_subscript( \
                                 id INT,                        \
                                 name VARCHAR(64),              \
                                 start_date DATE,               \
                                 payment_date DATE,             \
                                 payment INT,                   \
                                 accumulate_payment INT,        \
                                 signout_info INT)"             

            

            create_subscripts_groups = f""
