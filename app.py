from flask import Flask, request, send_file
import os, subprocess, uuid, shutil

app = Flask(__name__)
UPLOAD = 'uploads'
REPORTS = 'reports'
os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(REPORTS, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        apk = request.files['apk']
        uid = str(uuid.uuid4())
        apk_path = os.path.join(UPLOAD, f"{uid}.apk")
        apk.save(apk_path)

        out_dir = os.path.join(REPORTS, uid)
        os.makedirs(out_dir)

        # MobSF (basic static scan)
        subprocess.run([
    "docker", "run", "--rm",
    "-v", f"{os.getcwd()}:/workspace",
    "opensecurity/mobsf:latest",
    "python3", "/home/mobsf/Mobile-Security-Framework-MobSF/manage.py", "scan",
    "--file", f"/workspace/{os.path.basename(apk_path)}",
    "--output", f"/workspace/{uid}"
]))

        shutil.make_archive(out_dir, 'zip', out_dir)
        return send_file(f"{out_dir}.zip", as_attachment=True)

    return '''
    <h2>APKVulnBot – Upload APK</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="apk" accept=".apk" required>
        <button type="submit">Scan</button>
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
