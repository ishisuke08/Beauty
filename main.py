from flask import Flask, request, render_template

app = Flask(__name__)

# 美容液のデータベース（本来は別ファイルやDBで管理すると綺麗です）
SERUM_DATA = {
    "rough": {"name": "ドクダミ77スージングセラム", "desc": "鎮静・トラブルケア"},
    "pore": {"name": "桃70ナイアシンセラム", "desc": "ゴワつき・肌キメケア"},
    "acne": {"name": "アゼライン酸15インテンスカーミングセラム", "desc": "皮脂抑制・ニキビケア"},
    "spot": {"name": "ダークスポットセラム", "desc": "色素沈着・乾燥ケア"},
    "dull": {"name": "ビタミン10セラム", "desc": "美白・毛穴ケア"},
    "dry": {"name": "PDRNヒアルロン酸カプセル100セラム", "desc": "ツヤ出し・水光ケア"},
    "aging": {"name": "レチノール0.3ナイアシンリニューイングセラム", "desc": "毛穴・エイジングケア"},
    "oil": {"name": "シラカバ70ブースティングセラム", "desc": "高保湿・うるおいケア"},
    "texture": {"name": "7ライスセラミドグロウセラム", "desc": "トーンアップ・肌バリアケア"}
}

# 1. プロジェクトのトップ
@app.route('/')
def index():
    return render_template('index.html')


# 2. 悩み選択
@app.route('/anua')
def anua():
    return render_template('anua_form.html')


# 3. じゃんけんデータ送信先とじゃんけん結果表示画面
@app.route('/anua/result', methods=["POST"])
def anua_result():
    # JavaScriptから "rough,pore" のようなカンマ区切りの文字列で届く
    selected_str = request.form.get("skin_trouble", "")
    
    # カンマで分割してリストにする -> ['rough', 'pore']
    troubles = selected_str.split(",") if selected_str else []
    
    # 選ばれたすべての悩みに対する美容液データを集める
    recommended_products = []
    for trouble in troubles:
        product = SERUM_DATA.get(trouble)
        if product and product not in recommended_products: # 重複を防ぐ
            recommended_products.append(product)
            
    # もし何も選ばれていなければ、デフォルトでドクダミを入れる
    if not recommended_products:
        recommended_products.append(SERUM_DATA["rough"])
        
    # 結果画面に「リスト」として渡す
    return render_template('anua_result.html', products=recommended_products)

if __name__ == '__main__':
    # portは適宜書き換えてください
    app.run(host="0.0.0.0", port=1234, debug=True)