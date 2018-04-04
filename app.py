from flask import Flask, request, redirect, url_for, abort, Response, render_template
from io import BytesIO
from PIL import Image
import os
import json
import hashlib, datetime
import server.utility.StorageWrapper

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['JPG', 'jpg'])

app = Flask(__name__)

@app.route("/")
def page_top():
    return render_template("sample.html")

@app.route("/image")
def disp():
    try:
        image = Image.open(request.args.get('key', '') + ".png")
    except IOError:
        abort(404)
        
    output = BytesIO()

    image.save(output, format='png')
    return Response(response=output.getvalue(), content_type='image/png')

@app.route("/api", methods=['POST'])
def page_api():
    if request.method == 'POST':
        if (request.form['type'] == 'upload_image'):
            image_num = int(request.form['num'])
            print(str(image_num))

            now = datetime.datetime.now()
            namehead = hashlib.sha224((now.strftime("%Y%m%d%H%M%S.") + "%04d" % (now.microsecond // 1000)).encode('utf-8')).hexdigest()

            i = 0
            while (i < image_num):
                name_image = 'img' + str(i)
                uploaded_image = request.files[name_image]
                # save the file
                if (is_allowed_filetype(uploaded_image.filename)):
                    print("uploading: " + name_image)
                    output = BytesIO()
                    uploaded_image.save(output)
                    sw = src.utility.StorageWrapper.StorageWrapper()
                    sw.put_image(namehead + "/" + name_image + ".jpg", output.getvalue())
                    print("done")
                i += 1

            return json.dumps({'result':'OK'})

        return json.dumps({'result':'NG'})
    else:
        abort(401);

def is_allowed_filetype(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True);

