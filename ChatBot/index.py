import os
# import bot_files.LCMetaData as LCMetaData
import bot_files.NewQuestion as NewQuestion
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename#For File upload
chatHistoryFlag = 0
app = Flask(__name__)

#File Upload Config
app.secret_key = "1234"
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'files')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['pdf'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# WebPage routing
@app.route("/")
def home():
    global chatHistoryFlag
    chatHistoryFlag = 1
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    global chatHistoryFlag
    userText = request.args.get('msg')
    # return str(LCMetaData.print_answer2(userText))
    out = NewQuestion.print_answer(userText,chatHistoryFlag)
    chatHistoryFlag = 0
    response = str(out[0]) 
    #Uncomment to add sources
    #response += "The source files are:"
    # for i in out[1]:
    #     response= response + i + ", "     
    return response

@app.route('/upload-files')
def upload_form():
    return render_template('upload.html')


@app.route('/upload-files', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        existingFiles = os.listdir('files/')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if file not in existingFiles:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File(s) successfully uploaded')
        return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,threaded=True,debug=False)
    
#LCMetaData.print_answer2("Who is the best choice for php development")