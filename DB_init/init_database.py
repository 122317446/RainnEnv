from DAO.testDAO import testDAO

def initialise_database():
    heading_dao = testDAO(db_name="website.db")

    print("The test DB is initalised!")

    heading_dao.close_connection()


if __name__ == "__main__":
    initialise_database()