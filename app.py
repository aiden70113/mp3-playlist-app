from flask import Flask, render_template, request, send_file
from pydub import AudioSegment
import os
import tempfile

app = Flask(__name__)
UPLOAD_FOLDER = tempfile.gettempdir()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        files = request.files.getlist("mp3files")
        playlist_name = request.form.get("playlist_name", "merged_playlist")
        sort_order = request.form.get("sort_option", "이름순")

        paths = []
        for file in files:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            paths.append(filepath)

        if sort_order == "이름순":
            paths.sort()
        elif sort_order == "업로드 순":
            pass  # 업로드 순 유지

        combined = AudioSegment.empty()
        for path in paths:
            audio = AudioSegment.from_mp3(path)
            combined += audio

        output_path = os.path.join("static", f"{playlist_name}.mp3")
        combined.export(output_path, format="mp3")

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")
