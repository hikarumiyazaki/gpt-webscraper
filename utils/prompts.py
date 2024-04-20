GET_KEYWORD_AND_QUESTIONS = """
ユーザーからプロンプトが与えられます。json形式で回答してください。
回答できる場合は、is_answered=trueとして、responseに回答を記載してください。
インターネットで情報を取得する必要がある場合は、is_answered=falseとして、keywordに検索ワードを記載し、requestにユーザーのリクエストを記載してください。

例を参考にしてください。

# プロンプト
{message}

# 出力形式
{{
    "is_answered": boolean,
    "keyword": "[検索ワード]",
    "response": "[ユーザーの求めるデータ]"
}}

# 例
## メッセージ
"Pythonのリストの要素を削除する方法を教えてください"

## レスポンス
{{
    "is_answered": true,
    "keyword": null,
    "response": "del文を使用することでリストから要素を削除することができます。"
}}

## メッセージ
"2024年の杉花粉の飛散予想を教えてください"

## レスポンス
{{
    "is_answered": false,
    "keyword": "2024年 杉花粉 飛散 予想",
    "response": null
}}
"""

GET_ANSWER = """
ユーザーのリクエストに対して、回答を生成してください。
参考となるhtmlソースを提示します。
回答は、htmlソースとユーザーの質問を元に生成してください。
また、
生成した回答を出力形式に記載されたjson形式で返却してください。
例を参考にしてください。

# ユーザーのリクエスト
{request}

# htmlソース
{html_source}

# 出力形式

{{
    "response": "[回答]",
    "is_answered": boolean
}}

# 例
## ユーザーのリクエスト
"Pythonのリストの要素を削除する方法を教えてください"

## htmlソース
"<html><body><h1>Pythonのリストの要素を削除する方法</h1>delを使うといいぞい</body></html>"


## レスポンス
{{
    "response": "リストから要素を削除するには、del文を使用します。",
    "is_answered": true
}}

## ユーザーのリクエスト
"2220年の杉花粉の飛散予想を教えてください"

## htmlソース
"<html><body><h1>2220年のスギ花粉飛散量</h1>未来すぎてわからんぞい</body></html>"

## レスポンス
{{
    "response": "情報が見つかりませんでした。",
    "is_answered": false
}}

"""
