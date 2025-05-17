from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Baixar YouTube</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            text-align: center;
            padding: 30px;
        }
        h2 {
            color: #333;
        }
        form {
            background-color: #fff;
            padding: 20px;
            margin-top: 20px;
            border-radius: 10px;
            display: inline-block;
            max-width: 100%;
            width: 90%;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        input[type="text"], select {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border-radius: 6px;
            border: 1px solid #ccc;
            font-size: 16px;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 14px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        .footer {
            margin-top: 40px;
            color: #888;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <h2>Baixar vídeo do YouTube</h2>
    <form method="POST">
        <input type="text" name="url" placeholder="Cole o link do vídeo aqui" required><br>
        <select name="formato">
            <option value="mp4">MP4 (vídeo)</option>
            <option value="m4a">M4A (áudio)</option>
        </select><br>
        <input type="submit" value="Baixar">
    </form>
    <div class="footer">Desenvolvido por Lucas com Flask + yt_dlp</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        formato = request.form.get('formato')

        output_dir = '/tmp'
        
        cookies_path = 'cookies.txt'

        # Configurações conforme o formato escolhido
        if formato == 'm4a':
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'cookiefile': cookies_path,
            }
        else:  # mp4
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'cookiefile': cookies_path,
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title')
                ext = 'm4a' if formato == 'm4a' else 'mp4'
                final_path = os.path.join(output_dir, f"{title}.{ext}")

            if os.path.exists(final_path):
                return send_file(final_path, as_attachment=True)
            else:
                return f"Erro: arquivo não encontrado em {final_path}"
        except Exception as e:
            return f"Erro ao baixar: {str(e)}"

    return render_template_string(HTML_FORM)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
