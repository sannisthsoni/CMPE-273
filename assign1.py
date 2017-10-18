from flask import Flask
import rocksdb
import subprocess
from flask import abort
from flask import make_response
from flask import request
import rocksdb
import uuid


app = Flask(__name__)

@app.route('/api/v1/scripts',methods=['POST'])
def upload_file():
	if request.method == 'POST':
		db = rocksdb.DB("assign1.db",rocksdb.Options(create_if_missing = True))
		key = uuid.uuid4().hex
		f = request.files['data']
		path = '/tmp/' + key + ".py"
		f.save(path)
		db.put(key.encode('utf-8'),path.encode('utf-8'))
		return (key,201)

@app.route('/api/v1/scripts/<script_id>', methods=['GET'])
def get_output(script_id):
	if request.method == 'GET':
		db = rocksdb.DB("assign1.db",rocksdb.Options(create_if_missing = True))
		fname = db.get(script_id.encode('utf-8'))
		f_name = str(fname)
		temp = len(f_name)-3
		command = "python3 "+ '"' + f_name[2:temp] + "py" + '"'
		p = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
		return p.stdout.readline()
		
		



if __name__ == '__main__':
    app.run(debug=True)
