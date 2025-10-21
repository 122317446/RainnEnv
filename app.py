from flask import*
from service.UserinputsService import UserinputsService
from model.testModel import Userinputs

app = Flask(__name__)
userinputservice = UserinputsService()

@app.route("/")
def test1():
    data = userinputservice.get_all_data()
    print(data)
    return render_template('index.html', data=data)

  
@app.route('/add_data', methods=['POST'])
def add_data():
    new_data = Userinputs(
        None,
        request.form.get('addtext')
    )

    userinputservice.add_data(new_data)

    print("Received and instered into db!")

    return redirect(url_for("test1"))

@app.route('/get_data_by_id/<int:ID>')
def retreive_specific_data(ID):
    retreived = userinputservice.get_data_details(ID)
    return render_template('indexid.html', retreived=retreived)

@app.route('/update_data/<int:ID>', methods=['POST'])
def update_data(ID):
    retreived = userinputservice.get_data_details(ID)

    retreived.text = request.form.get('changetext')

    userinputservice.update_data(retreived)

    print("The database has been updated!")

    return redirect(url_for("test1"))

@app.route('/delete_data/<int:ID>', methods=['POST'])
def delete_data(ID):
    userinputservice.delete_data(ID)
    print("Data entry has been deleted!")

    return redirect(url_for("test1"))
