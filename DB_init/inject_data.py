from DAO.testDAO import testDAO
from model.testModel import Userinputs

def inject_sample_data():
    heading_dao = testDAO(db_name="website.db")

    example1 = Userinputs(None, 'Karl')
    heading_dao.add_Userinputs(example1)

    example2 = Userinputs(None, 'Russel')
    heading_dao.add_Userinputs(example2)

    heading_dao.close_connection()

    print("Sample data has been added to the database!")

if __name__ == "__main__":
    inject_sample_data()

