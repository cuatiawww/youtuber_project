from flask import Flask, render_template, request, jsonify, send_from_directory
from pytrends.request import TrendReq
from datetime import datetime
import pandas as pd
import time
from pytrends.exceptions import ResponseError  
import random
import requests
import os
import traceback

app = Flask(__name__)
pytrends = TrendReq(hl='id-ID', tz=360)
API_KEY = "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"
YOUTUBE_API_KEY = "AIzaSyDrwRrCYfhev87uSzwDxR3LRq1I0rQtwIw"
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"
app.config['TEMPLATES_AUTO_RELOAD'] = True

GAMES = ["Mobile Legends", "PUBG", "Free Fire", "Resident Evil", "League of Legends", "Valorant"]

# Debug function
def debug_templates():
    templates_dir = os.path.join(app.root_path, 'templates')
    static_dir = os.path.join(app.root_path, 'static')
    
    print(f"App root path: {app.root_path}")
    print(f"Templates directory: {templates_dir}")
    print(f"Templates exists: {os.path.exists(templates_dir)}")
    print(f"Static directory: {static_dir}")
    print(f"Static exists: {os.path.exists(static_dir)}")
    
    if os.path.exists(templates_dir):
        print("Template files:", os.listdir(templates_dir))
    if os.path.exists(static_dir):
        print("Static directories:", os.listdir(static_dir))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    print(f"404 Error: {error}")
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>404 - Not Found</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white min-h-screen flex items-center justify-center">
        <div class="text-center">
            <h1 class="text-4xl font-bold text-red-400 mb-4">404 - Page Not Found</h1>
            <p class="text-gray-300 mb-4">Halaman yang Anda cari tidak ditemukan.</p>
            <p class="text-sm text-gray-500 mb-4">Error: {error}</p>
            <a href="/" class="bg-sky-500 hover:bg-sky-600 px-4 py-2 rounded text-white">Kembali ke Beranda</a>
        </div>
    </body>
    </html>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    print(f"500 Error: {error}")
    print(traceback.format_exc())
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>500 - Internal Error</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white min-h-screen flex items-center justify-center">
        <div class="text-center">
            <h1 class="text-4xl font-bold text-red-400 mb-4">500 - Internal Server Error</h1>
            <p class="text-gray-300 mb-4">Terjadi kesalahan pada server.</p>
            <p class="text-sm text-gray-500 mb-4">Error: {error}</p>
            <a href="/" class="bg-sky-500 hover:bg-sky-600 px-4 py-2 rounded text-white">Kembali ke Beranda</a>
        </div>
    </body>
    </html>
    """, 500

@app.route('/debug')
def debug():
    debug_templates()
    return "Check console for debug info"

@app.route('/')
def dashboard():
    """Renders the dashboard page."""
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error loading dashboard: {e}")
        print(traceback.format_exc())
        return f"Error loading dashboard: {e}<br><a href='/debug'>Debug Info</a>", 500

@app.route('/analytic')
def analytic():
    """Renders the analytic page."""
    try:
        return render_template('analytic.html')
    except Exception as e:
        print(f"Error loading analytic: {e}")
        return f"Template analytic.html not found: {e}<br><a href='/debug'>Debug Info</a>", 404

# Simple template routes for testing
@app.route("/ml")
def mobile_legends():
    try:
        return render_template("ml.html")
    except:
        return """
        <!DOCTYPE html>
        <html><head><title>Mobile Legends</title><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-slate-900 text-white p-8">
            <h1 class="text-3xl font-bold text-sky-400">Mobile Legends</h1>
            <p class="text-gray-300 mt-4">Halaman detail Mobile Legends sedang dikembangkan.</p>
            <a href="/" class="mt-4 inline-block bg-sky-500 px-4 py-2 rounded">Kembali</a>
        </body></html>
        """

@app.route("/pubg")
def pubg():
    try:
        return render_template("pubg.html")
    except:
        return """
        <!DOCTYPE html>
        <html><head><title>PUBG</title><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-slate-900 text-white p-8">
            <h1 class="text-3xl font-bold text-sky-400">PUBG</h1>
            <p class="text-gray-300 mt-4">Halaman detail PUBG sedang dikembangkan.</p>
            <a href="/" class="mt-4 inline-block bg-sky-500 px-4 py-2 rounded">Kembali</a>
        </body></html>
        """

@app.route("/re")
def resident_evil():
    try:
        return render_template("re.html")
    except:
        return """
        <!DOCTYPE html>
        <html><head><title>Resident Evil</title><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-slate-900 text-white p-8">
            <h1 class="text-3xl font-bold text-sky-400">Resident Evil</h1>
            <p class="text-gray-300 mt-4">Halaman detail Resident Evil sedang dikembangkan.</p>
            <a href="/" class="mt-4 inline-block bg-sky-500 px-4 py-2 rounded">Kembali</a>
        </body></html>
        """

@app.route('/lol')
def lol_detail():
    try:
        return render_template('lol.html')
    except:
        return """
        <!DOCTYPE html>
        <html><head><title>League of Legends</title><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-slate-900 text-white p-8">
            <h1 class="text-3xl font-bold text-sky-400">League of Legends</h1>
            <p class="text-gray-300 mt-4">Halaman detail League of Legends sedang dikembangkan.</p>
            <a href="/" class="mt-4 inline-block bg-sky-500 px-4 py-2 rounded">Kembali</a>
        </body></html>
        """

@app.route('/freefire')
def freefire_detail():
    try:
        return render_template('freefire.html')
    except:
        return """
        <!DOCTYPE html>
        <html><head><title>Free Fire</title><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-slate-900 text-white p-8">
            <h1 class="text-3xl font-bold text-sky-400">Free Fire</h1>
            <p class="text-gray-300 mt-4">Halaman detail Free Fire sedang dikembangkan.</p>
            <a href="/" class="mt-4 inline-block bg-sky-500 px-4 py-2 rounded">Kembali</a>
        </body></html>
        """

@app.route('/valorant')
def valorant_detail():
    try:
        return render_template('valorant.html')
    except:
        return """
        <!DOCTYPE html>
        <html><head><title>Valorant</title><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-slate-900 text-white p-8">
            <h1 class="text-3xl font-bold text-sky-400">Valorant</h1>
            <p class="text-gray-300 mt-4">Halaman detail Valorant sedang dikembangkan.</p>
            <a href="/" class="mt-4 inline-block bg-sky-500 px-4 py-2 rounded">Kembali</a>
        </body></html>
        """

@app.route('/title')
def judul_video():
    try:
        return render_template('title.html')
    except:
        return """
        <!DOCTYPE html>
        <html><head><title>Title Generator</title><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-slate-900 text-white p-8">
            <h1 class="text-3xl font-bold text-sky-400">Title Generator</h1>
            <p class="text-gray-300 mt-4">Halaman Title Generator sedang dikembangkan.</p>
            <a href="/" class="mt-4 inline-block bg-sky-500 px-4 py-2 rounded">Kembali</a>
        </body></html>
        """

@app.route('/trending')
def trending_page():
    try:
        return render_template('trending.html')
    except:
        return """
        <!DOCTYPE html>
        <html><head><title>Trending</title><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-slate-900 text-white p-8">
            <h1 class="text-3xl font-bold text-sky-400">Trending Games</h1>
            <p class="text-gray-300 mt-4">Halaman Trending sedang dikembangkan.</p>
            <a href="/" class="mt-4 inline-block bg-sky-500 px-4 py-2 rounded">Kembali</a>
        </body></html>
        """

@app.route('/search')
def search_page():
    try:
        return render_template('search.html')
    except:
        return """
        <!DOCTYPE html>
        <html><head><title>Search</title><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-slate-900 text-white p-8">
            <h1 class="text-3xl font-bold text-sky-400">Search Games</h1>
            <p class="text-gray-300 mt-4">Halaman Search sedang dikembangkan.</p>
            <a href="/" class="mt-4 inline-block bg-sky-500 px-4 py-2 rounded">Kembali</a>
        </body></html>
        """

@app.route('/get_trend_data')
def get_trend_data():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)

        keywords_batch1 = ["Mobile Legends", "PUBG", "Free Fire", "Resident Evil", "League Of Legends"]
        keywords_batch2 = ["Valorant"]

        range_days = int(request.args.get('range', 1))

        if range_days == 1:
            timeframe = 'now 1-d'
        elif range_days == 7:
            timeframe = 'now 7-d'
        elif range_days == 30:
            timeframe = 'today 1-m'
        else:
            timeframe = 'today 3-m'

        # Batch pertama
        pytrends.build_payload(keywords_batch1, timeframe=timeframe, geo='ID')
        df1 = pytrends.interest_over_time()

        # Batch kedua
        if keywords_batch2:
            pytrends.build_payload(keywords_batch2, timeframe=timeframe, geo='ID')
            df2 = pytrends.interest_over_time()
            df = pd.concat([df1[keywords_batch1], df2[keywords_batch2]], axis=1)
            df["date"] = df1.index
        else:
            df = df1
            df["date"] = df.index

        df.reset_index(drop=True, inplace=True)

        results = {}
        for keyword in keywords_batch1 + keywords_batch2:
            results[keyword] = [
                {"time": row["date"].isoformat(), "score": row[keyword]}
                for _, row in df.iterrows()
            ]
        return jsonify(results)
    except Exception as e:
        print(f"Error in get_trend_data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/rekomendasi-judul", methods=["GET", "POST"])
def rekomendasi_judul():
    if request.method == "POST":
        try:
            game_name = request.form["game"]
            prompt = f"Buatkan 5 judul YouTube yang menarik, SEO-friendly, dan click-worthy untuk video tentang game {game_name}, seolah-olah dibuat oleh YouTuber gaming yang ingin viral."

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Kamu adalah ahli strategi YouTube untuk konten game."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 500
            }
            
            response = requests.post(DEEPSEEK_ENDPOINT, headers=headers, json=data)
            response.raise_for_status()
            hasil = response.json()
            generated_text = hasil['choices'][0]['message']['content']
            
            try:
                return render_template("rekomendasi_judul.html", judul_list=generated_text.split("\n"), game=game_name)
            except:
                return f"""
                <!DOCTYPE html>
                <html><head><title>Rekomendasi Judul</title><script src="https://cdn.tailwindcss.com"></script></head>
                <body class="bg-slate-900 text-white p-8">
                    <h1 class="text-3xl font-bold text-sky-400">Rekomendasi Judul untuk {game_name}</h1>
                    <div class="mt-4">
                        {"<br>".join(generated_text.split("\n"))}
                    </div>
                    <a href="/title" class="mt-4 inline-block bg-sky-500 px-4 py-2 rounded">Kembali</a>
                </body></html>
                """
        except Exception as e:
            return f"""
            <!DOCTYPE html>
            <html><head><title>Error</title><script src="https://cdn.tailwindcss.com"></script></head>
            <body class="bg-slate-900 text-white p-8">
                <h1 class="text-3xl font-bold text-red-400">Error</h1>
                <p class="text-gray-300 mt-4">Error: {str(e)}</p>
                <a href="/title" class="mt-4 inline-block bg-sky-500 px-4 py-2 rounded">Kembali</a>
            </body></html>
            """

    try:
        return render_template("rekomendasi_judul.html")
    except:
        return """
        <!DOCTYPE html>
        <html><head><title>Rekomendasi Judul</title><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-slate-900 text-white p-8">
            <h1 class="text-3xl font-bold text-sky-400">Rekomendasi Judul YouTube</h1>
            <form method="POST" class="mt-6">
                <div class="mb-4">
                    <label class="block text-gray-300 mb-2">Pilih Game:</label>
                    <select name="game" class="bg-slate-800 text-white p-2 rounded w-full">
                        <option value="Mobile Legends">Mobile Legends</option>
                        <option value="PUBG">PUBG</option>
                        <option value="Free Fire">Free Fire</option>
                        <option value="Valorant">Valorant</option>
                        <option value="League of Legends">League of Legends</option>
                    </select>
                </div>
                <button type="submit" class="bg-sky-500 hover:bg-sky-600 px-6 py-2 rounded text-white">Generate Judul</button>
            </form>
            <a href="/" class="mt-4 inline-block bg-gray-600 px-4 py-2 rounded">Kembali</a>
        </body></html>
        """

@app.route("/trending_games")
def get_trending_games():
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "chart": "mostPopular",
        "regionCode": "ID",
        "videoCategoryId": "20",
        "maxResults": 9,
        "key": YOUTUBE_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "items" not in data:
            return jsonify({"videos": []})

        videos = []
        for item in data["items"]:
            videos.append({
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                "channel": item["snippet"]["channelTitle"],
                "url": f"https://www.youtube.com/watch?v={item['id']}"
            })

        return jsonify({"videos": videos})
    except Exception as e:
        print("Error:", e)
        return jsonify({"videos": []})

@app.route("/search_game")
def search_game():
    try:
        game = request.args.get("game")
        if not game:
            return jsonify({"error": "No game provided"}), 400

        pytrends.build_payload([game], cat=0, timeframe='today 3-m')
        data = pytrends.interest_over_time()

        if data.empty:
            return jsonify({"labels": [], "scores": [], "game": game})

        labels = [dt.strftime('%Y-%m-%d') for dt in data.index]
        scores = data[game].tolist()

        return jsonify({
            "labels": labels,
            "scores": scores,
            "game": game
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Test route
@app.route('/test')
def test():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white p-8">
        <h1 class="text-3xl font-bold text-green-400">✅ Flask App is Working!</h1>
        <div class="mt-4 space-y-2">
            <p><a href="/" class="text-sky-400 hover:underline">🏠 Dashboard</a></p>
            <p><a href="/analytic" class="text-sky-400 hover:underline">📊 Analytics</a></p>
            <p><a href="/title" class="text-sky-400 hover:underline">🏆 Title Generator</a></p>
            <p><a href="/trending" class="text-sky-400 hover:underline">🔥 Trending</a></p>
            <p><a href="/search" class="text-sky-400 hover:underline">🔍 Search</a></p>
            <p><a href="/debug" class="text-yellow-400 hover:underline">🔧 Debug Info</a></p>
        </div>
    </body>
    </html>
    """

# VERCEL COMPATIBILITY - Pastikan ini ada untuk Vercel
# Vercel akan mencari variable 'app' sebagai WSGI app
if __name__ == '__main__':
    print("="*50)
    print("🎮 GameTrend Flask App Starting...")
    print("="*50)
    
    # Debug info
    debug_templates()
    
    print("\n📍 Available routes:")
    print("   • http://localhost:5000/ (Dashboard)")
    print("   • http://localhost:5000/test (Test page)")
    print("   • http://localhost:5000/debug (Debug info)")
    print("   • http://localhost:5000/analytic (Analytics)")
    print("\n🚀 Starting server...")
    
    app.run(debug=True, host='0.0.0.0', port=5000)