## プロジェクト概要
このプロジェクトは、未経験からWeb開発を学ぶために作成した学習用プロジェクトです。  
プロジェクトを通して、開発の流れや基本的な機能実装の経験を積むことを目的として開発をはじめました。

## アプリ概要
### 一般家庭のキッチンにある食材の在庫管理をするアプリ
賞味期限が切れる前に食材を消費し、食材を余らせることなく在庫管理しやすくする機能があります。

## 開発背景
家にある食材を計画的に使えず、期限切れにしてしまうことが多々ありました。  
冷蔵庫やキッチンにある食材の賞味期限は、現品のラベルを確認しないと把握できず、  
外出先では「何がどれくらい期限が近いのか」を確認できない点に不便さを感じていました。  
そこで、食材とその賞味期限を外出先からでも確認できるようにし、賞味期限が近い食材を  
優先的に使ったレシピを外出先からでも事前に考えられるツールを作りたいと考えました。

本アプリを利用することで
- 帰宅後すぐに調理に取り掛かることができる  
- 作りたい料理に不足している食材を帰宅途中で購入できる  
- 食材の賞味期限を一目で把握でき、食品ロスを減らせる  

このように、日常生活で感じていた食材管理のやりにくさを解消するため  
在庫の全体像を最新の状態で確認できるツールが欲しいと思い開発に至りました。

## 機能概要
### トップページ全体
![ページ全体](screenshots/whole_page.png)

### 食材＋賞味期限 の登録
食材名と賞味期限を登録できます。  
登録された食材＋賞味期限は一覧表示に追加されます。
![食材登録](screenshots/item_create.gif)

### 一覧表示と色分け表示機能
登録された食材と賞味期限が一覧表示されます。  
賞味期限までの残り日数に応じて食材ごとに色分け表示され、  
賞味期限が迫っている食材の緊急度を知らせる機能です。

＜色分けルール＞  
賞味期限切れ　　　　→　茶色表示＋⚠️  
賞味期限当日・前日　→　赤色表示  
賞味期限２日前　　　→　オレンジ色表示  
賞味期限３～５日前　→　緑色表示  
賞味期限６日以上前　→　デフォルト表示(黒色文字)  
![在庫一覧](screenshots/item_list.png)

### 食材・賞味期限 の 編集・削除
  登録した食材の削除ができます。  
![食材削除](screenshots/item_delete.gif)
![削除確認](screenshots/delete_confirm.png)

登録した食材の食材名・賞味期限が編集できます。
![食材編集](screenshots/item_edit.gif)
![編集画面](screenshots/item_edit_confirm.png)

### レシピ検索機能
消費したい食材を検索ボックスに入力して検索すると、  
その食材を使用したレシピの検索結果が一覧表示されます。  
賞味期限が迫っている食材を消費したいとき、レシピのアイデアを得るのに便利です。
![レシピ検索](screenshots/recipe_search.gif)
![レシピ一覧](screenshots/recipe_list.png)
![レシピ詳細](screenshots/recipe_detail.png)

#### 使用したAPI（レシピ検索用）
- Spoonacular API
  公式ドキュメント
  - キーワード検索用<br>Search Recipes (complexSearch): https://spoonacular.com/food-api/docs#Search-Recipes-Complex
  - レシピ詳細表示用<br>Get Recipe Information: https://spoonacular.com/food-api/docs#Get-Recipe-Information
  - その他参照元<br>https://spoonacular.com/food-api/docs#Authentication <br>https://spoonacular.com/food-api/docs#Quotas <br>https://spoonacular.com/food-api/docs#Show-Images

※APIキーは `.env` で管理し、リポジトリには含めません。

## 画面・URL設計
### 操作フロー
- アプリにアクセス：`/` → `/items/`（在庫一覧画面へ）
- 在庫を登録：`/items/` で食品名・賞味期限を入力 → 登録 → 一覧に反映
- 在庫を編集：一覧の「編集」→ 編集画面 → 保存 → 一覧へ戻る
- 在庫を削除：一覧の「削除」→ 確認画面 → 削除 → 一覧へ戻る
- レシピを探す：`/items/` 右カラムでキーワード検索 → 検索結果が右カラムだけ更新
- レシピ詳細を見る：検索結果のレシピをクリック → 詳細ページ → 戻る

### URL設計
本アプリは「在庫一覧 + 登録 + レシピ検索」を `/items/` に集約し、編集・削除・レシピ詳細のみ個別ページに分けています。  
また、レシピ検索はページ全体を再描画せず、右カラムのみ非同期で更新します。

|URL|Method|View|Response / Template|用途 / 補足|
|---|---:|---|---|---|
|`/`|GET| - |Redirect → `/items/`|ルートアクセスは一覧画面へ誘導|
|`/items/`|GET|`item_list`|ページHTML<br>`item_list.html`|在庫一覧 + 登録フォーム + レシピ検索UIを表示|
|`/items/`|POST|`item_list`|Redirect → `/items/`|アイテム登録（PRGパターンで二重送信を防止）|
|`/items/edit/<int:pk>/`|GET|`item_edit`|ページHTML<br>`item_edit.html`|編集フォーム表示|
|`/items/edit/<int:pk>/`|POST|`item_edit`|Redirect → `/items/`|編集内容を保存して一覧へ戻る|
|`/items/delete/<int:pk>/`|GET|`item_delete`|ページHTML<br>`item_confirm_delete.html`|削除確認画面（誤削除防止）|
|`/items/delete/<int:pk>/`|POST|`item_delete`|Redirect → `/items/`|削除実行して一覧へ戻る|
|`/items/recipe-search/`|GET|`recipe_search`|部分HTML<br>`_recipe_results.html`|JS(fetch)で呼び出し、レシピ検索結果部分のみ差し替え|
|`/items/recipe/<int:recipe_id>/`|GET|`recipe_detail`|ページHTML<br>`recipe_detail.html`|レシピ詳細表示（取得できない場合は404）|

### 非同期更新（右カラム差し替え）
`/items/recipe-search/?q=...` はページ全体ではなく **検索結果のHTML断片（partial）** を返します。  
`inventory/static/inventory/app.js` から fetch し、返ってきたHTMLを `#recipe-results` に差し込むことで右カラムのみ更新します。

## 設計で苦労した点
この在庫管理アプリでは、ユーザー体験の観点から以下の要件を満たしたく、UI上の制約がありました。
- 一覧表示を確認しながら食材アイテムを登録したい(一覧画面と登録画面が別だと操作が煩雑になるため)
- 在庫一覧表示画面で期限の迫っているアイテムを確認しながらレシピ検索ができるようにしたい<br>⇒アイテム登録・一覧表示・レシピ検索といった異なる処理を同一URLに集約する構成

一方で、設計上の方針
- エンドポイントが増えると導線や保守が複雑になりやすいため、1つのURLに対して入り口となるビューは<br>1つにとどめたい

先述のUI要件とこの設計方針(1URLに対し1ビュー)を同時に実現しようとすると、
ビュー関数に以下のすべてが混在することになってしまい、可読性や管理(テストや変更など)の煩雑さが問題でした。
- フォームのPOST処理（アイテム登録）
- DBからの一覧取得
- 外部API呼び出し（レシピ検索）
- 画面描画（テンプレートへの受け渡し）

そこで、URL構造は維持したままviews.pyの責務分離を実現するため、以下の構成にすることで対策しました。
- ビューはGET/POSTの分岐、リダイレクト、レスポンスを返すなど「HTTPリクエストの制御」に専念させる
- 実際の処理の中身は役割ごとに分割し、service層に取り出してビューから呼び出す

この対策により、UI要件は維持したまま、保守性・拡張性も考慮した設計にしました。
<details>
<summary>コード例（views.py：HTTP制御に専念し、処理はservice層へ委譲）</summary>

```python
# inventory/views.py
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import InventoryItemForm
from .services.inventory_service import get_items
from .services.spoonacular_service import search_recipes

@require_http_methods(["GET", "POST"])
def item_list(request):
    # ---------- アイテム登録（POST） ----------
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:item_list")
    else:
        form = InventoryItemForm()

    # ---------- 一覧取得（service層） ----------
    items = get_items()

    # ---------- レシピ検索（service層） ----------
    keyword = request.GET.get("q", "").strip()
    recipes = search_recipes(keyword)

    # ---------- レスポンス返却（テンプレへ受け渡し） ----------
    return render(request, "inventory/item_list.html", {
        "form": form,
        "items": items,
        "recipes": recipes,
        "keyword": keyword,
    })
```
</details><details><summary>コード例（service層：DB取得の切り出し）</summary>

```python
# inventory/services/inventory_service.py
from django.db.models import QuerySet
from ..models import InventoryItem

def get_items() -> QuerySet[InventoryItem]:
    return InventoryItem.objects.all().order_by("-id")
```
</details><details><summary>コード例（service層：外部API呼び出しの切り出し：検索）</summary>

```python
# inventory/services/spoonacular_service.py（検索）
from typing import Dict, List
import requests
from django.conf import settings

def search_recipes(keyword: str, number: int = 10) -> List[Dict]:
    if not keyword:
        return []

    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {"apiKey": settings.SPOONACULAR_API_KEY, "query": keyword, "number": number}

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
    except requests.RequestException:
        return []

    return [
        {"title": r.get("title"), "id": r.get("id"), "image": r.get("image")}
        for r in (data.get("results", []) or [])
    ]
```
</details>

## その他設計で工夫した点
### 1. 秘密情報はコードに直接書かない（環境変数 + .env）
外部APIキーやDjangoのSECRET_KEYは、公開リポジトリに秘密情報が含まれないよう、`.env` を読み込み、<br>環境変数から取得する設計にしています。

### 2. アイテムの削除は確認画面を挟み、うっかり削除を防止
削除機能は `GET=確認画面表示 / POST=削除実行` に分けています。  
削除URLを開いただけ(GETだけ)では削除は実行されないので、意図しない削除を防止します。
<details> <summary>コード例（views.py：GET=確認画面 / POST=削除実行）</summary>

```python
# inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import InventoryItem

def item_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect("inventory:item_list")
    return render(request, "inventory/item_confirm_delete.html", {"item": item})
```
</details> <details> <summary>コード例（item_confirm_delete.html：削除はPOSTでのみ送信）</summary>

```html
<!-- inventory/templates/inventory/item_confirm_delete.html -->
<form method="post">
  {% csrf_token %}
  <button class="btn btn-danger" type="submit">削除</button>
  <a class="btn" href="{% url 'inventory:item_list' %}" style="margin-left: 8px;">キャンセル</a>
</form>
```
</details>

### 3. アイテムの編集・削除はPRGパターンによりPOST二重送信を防止
削除・編集のPOST処理後にリダイレクトし、その後GETで一覧表示画面を表示させることで、<br>リロードによるPOST再送を防止します。
<details> <summary>コード例（views.py：PRG：編集 POST後にredirect）</summary>

```python
# inventory/views.py（編集）
def item_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("inventory:item_list")
    else:
        form = InventoryItemForm(instance=item)
    return render(request, "inventory/item_edit.html", {"form": form})
```
</details>

### 4. 日付計算ロジックはモデルに寄せ、テンプレートで計算しない
賞味期限の残日数は models.py の `InventoryItem.days_left`（property）で計算し、テンプレートでは計算せず、<br>表示に必要な `item.days_left` を参照するだけにしています。  
View/Service側で日付計算を毎回書かずに済むため、修正箇所を減らせるようにしました。

### 5. レシピ検索は部分更新用エンドポイントを分ける
在庫一覧を表示させたまま検索結果も閲覧できるようにしたかったため、検索結果ページへ遷移する形は避けました。
一方で、検索のたびに画面全体が再読み込みされるのを避けるため、検索結果だけ返す専用エンドポイントを用意し、検索結果（部分テンプレ）だけ返して右カラムを差し替える方式にしました。

- `/items/recipe-search/`：検索結果の **部分HTML**（`_recipe_results.html`）のみ返す
- `app.js`：fetchで取得し、`#recipe-results` だけ差し替え

また、検索結果の表示を`_recipe_results.html`に切り出したことで、保守性がUPしました。
<details> <summary>コード例（urls.py：部分更新用エンドポイント）</summary>

```python
# inventory/urls.py
from django.urls import path
from .views import recipe_search

urlpatterns = [
    path("recipe-search/", recipe_search, name="recipe_search"),
]
```
</details> <details> <summary>コード例（views.py：部分テンプレだけ返す）</summary>

```python
# inventory/views.py
from django.views.decorators.http import require_GET
from django.shortcuts import render
from .services.spoonacular_service import search_recipes

@require_GET
def recipe_search(request):
    keyword = request.GET.get("q", "").strip()
    recipes = search_recipes(keyword)
    return render(
        request,
        "inventory/_recipe_results.html",
        {"recipes": recipes, "keyword": keyword},
    )
```
</details> <details> <summary>コード例（item_list.html：フォームと差し替え先）</summary>

```html
<!-- inventory/templates/inventory/item_list.html（フォームと差し替え先） -->
<form id="recipe-search-form" data-endpoint="{% url 'inventory:recipe_search' %}">
  <div class="form-row">
    <input type="text" name="q" value="{{ keyword }}" placeholder="例：卵">
  </div>
  <button class="btn btn-primary" type="submit">検索</button>
</form>

<div id="recipe-results">
  {% include "inventory/_recipe_results.html" with recipes=recipes keyword=keyword %}
</div>
```
</details> <details> <summary>コード例（app.js：fetchで部分HTML取得→差し替え）</summary>

```javascript
// inventory/static/inventory/app.js
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const q = form.querySelector('input[name="q"]').value;

  try {
    const res = await fetch(endpoint + "?q=" + encodeURIComponent(q));
    const html = await res.text();
    results.innerHTML = html;
  } catch (err) {
    results.innerHTML = "<p>検索に失敗しました。通信状況を確認してもう一度お試しください。</p>";
  }
});
```
</details>

### 6. 外部APIの連携処理は「検索結果一覧表示」と「レシピ詳細」を分離<br>⇒失敗しても画面が壊れないように設計
Spoonacular APIは用途別に関数を分けています。
- `search_recipes()`：検索結果一覧表示用データを返す(成功時:list / 失敗時:空リスト[])
- `fetch_recipe_detail()`：レシピ詳細表示用データを返す(成功時:dict / 失敗時:`None`)

こうすることで、失敗時の挙動を用途ごとに最適化でき、例外がテンプレートまで伝播して500エラーになるのを防ぐことができます。
- `search_recipes()`：失敗時に空リストを返すことで検索結果部分だけを「0件表示」に着地させる
- `fetch_recipe_detail()`：失敗時に`None`を返し、View側で404(Not Found)として扱う

その結果、レシピ詳細の取得に失敗しても検索結果一覧や在庫リストまで巻き込まれず、
レシピ検索に失敗しても、在庫一覧・登録フォームは表示されたまま利用できます。
<details> <summary>コード例（spoonacular_service.py：検索は失敗時[] / 詳細は失敗時None）</summary>

```python
# inventory/services/spoonacular_service.py
from typing import Dict, List, Optional
import requests
from django.conf import settings

def search_recipes(keyword: str, number: int = 10) -> List[Dict]:
    if not keyword:
        return []

    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {"apiKey": settings.SPOONACULAR_API_KEY, "query": keyword, "number": number}

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
    except requests.RequestException:
        return []

    return [
        {"title": r.get("title"), "id": r.get("id"), "image": r.get("image")}
        for r in (data.get("results", []) or [])
    ]

def fetch_recipe_detail(recipe_id: int) -> Optional[Dict]:
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": settings.SPOONACULAR_API_KEY}

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.RequestException:
        return None
```
</details> <details> <summary>コード例（views.py：詳細がNoneなら404に着地）</summary>

```python
# inventory/views.py（Noneなら404に着地）
from django.http import Http404
from .services.spoonacular_service import fetch_recipe_detail

def recipe_detail(request, recipe_id):
    recipe = fetch_recipe_detail(recipe_id)
    if recipe is None:
        raise Http404("Recipe not found")
    return render(request, "inventory/recipe_detail.html", {"recipe": recipe})
```
</details>

## 学んだこと
- Webアプリ開発の基本的な仕組みと開発のおおまかな流れ
- Linuxの使い方
- 仮想環境の設定
- DB設計手法（正規化など）
- Djangoの基本的なCRUD処理の理解
- MVCモデル（MVTモデル）の考え方
- VS Codeの操作
- 簡単なフロントエンド表示（色分けなど）
- 外部APIの実装
- バグ修正や簡易機能修正
- Gitによるバージョン管理

## 今後の課題・改善点
- レシピ詳細ページの表示バグ修正
- 機能追加(賞味期限/消費期限の選択、レシピの保存、ダッシュボード、ユーザー認証など)
- テストの導入
- セキュリティ面の強化
- デプロイ未経験
- その他、認識できていない改善点や課題を調査中(特に、保守性・安全性などの設計観点ごとに調査中)

## 動作環境
- Python 3.11
- Django 5.0.14
- Ubuntu 22.04（WSL上）