import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 環境変数を読み込み
load_dotenv()

def get_llm_response(input_text: str, expert_type: str) -> str:
    """
    ユーザーの入力テキストと専門家タイプに基づいて、LLMからの回答を取得する関数
    
    Args:
        input_text (str): ユーザーの入力テキスト
        expert_type (str): 選択された専門家のタイプ
    
    Returns:
        str: LLMからの回答
    """
    # 専門家タイプに応じたシステムメッセージを設定
    system_messages = {
        "医師": "あなたは経験豊富な医師です。患者の症状や健康に関する質問に対して、医学的知識に基づいた適切で分かりやすいアドバイスを提供してください。ただし、最終的な診断や治療については必ず実際の医療機関での受診を勧めてください。日本語で回答してください。",
        "料理研究家": "あなたは経験豊富な料理研究家です。料理のレシピ、調理法、食材の選び方、栄養について専門的なアドバイスを提供してください。初心者にも分かりやすく、実践的な内容を心がけてください。日本語で回答してください。",
        "ITエンジニア": "あなたは経験豊富なITエンジニアです。プログラミング、システム開発、技術的な問題解決について専門的なアドバイスを提供してください。初心者から上級者まで理解できるよう、分かりやすく説明してください。日本語で回答してください。",
        "ファイナンシャルプランナー": "あなたは経験豊富なファイナンシャルプランナーです。投資、保険、税金、資産運用、家計管理について専門的なアドバイスを提供してください。個人の状況に応じた実践的なアドバイスを心がけてください。日本語で回答してください。"
    }
    
    try:
        # APIキーを取得し、未設定の場合はエラーを返す
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "エラー: OpenAI APIキーが設定されていません。サイドバーの手順に従ってAPIキーを設定してください。"

        # ChatOpenAIインスタンスを作成
        chat = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=api_key
        )
        
        # メッセージを作成
        messages = [
            SystemMessage(content=system_messages[expert_type]),
            HumanMessage(content=input_text)
        ]
        
        # LLMから回答を取得
        response = chat.invoke(messages)
        return response.content
        
    except Exception as e:
        # 開発者向けの詳細なエラーはログに出力
        import logging
        logging.error("LLM応答取得時に例外発生: %s", str(e))
        # ユーザーには簡潔なエラーメッセージのみ表示
        return "エラーが発生しました。しばらくしてから再度お試しください。"

def main():
    # ページ設定
    st.set_page_config(
        page_title="専門家AI相談アプリ",
        page_icon="🤖",
        layout="wide"
    )
    
    # アプリのタイトル
    st.title("🤖 専門家AI相談アプリ")
    
    # アプリの概要と操作方法
    st.markdown("""
    ## 📖 アプリの概要
    このアプリは、AIを活用した専門家相談システムです。4つの異なる分野の専門家として機能するAIに質問や相談をすることができます。
    
    ## 🔧 操作方法
    1. **専門家を選択**: 下のラジオボタンから相談したい分野の専門家を選んでください
    2. **質問を入力**: テキストエリアに相談したい内容を詳しく入力してください
    3. **相談開始**: 「相談する」ボタンをクリックしてAI専門家からの回答を受け取ってください
    
    ## 👨‍⚕️ 利用可能な専門家
    - **医師**: 健康・医療に関する相談
    - **料理研究家**: 料理・食材・栄養に関する相談
    - **ITエンジニア**: プログラミング・技術に関する相談
    - **ファイナンシャルプランナー**: 投資・資産運用・家計に関する相談
    
    ## ⚠️ 注意事項
    - このアプリはAIによる情報提供サービスです
    - 重要な決定については、実際の専門家にご相談ください
    - 緊急の場合は適切な機関に直接連絡してください
    
    ---
    """)
    
    # 専門家選択（ラジオボタン）
    st.subheader("👨‍💼 専門家を選択してください")
    expert_type = st.radio(
        "相談したい専門家の分野を選んでください:",
        ["医師", "料理研究家", "ITエンジニア", "ファイナンシャルプランナー"],
        horizontal=True,
        help="選択した専門家の分野に特化したアドバイスを受けることができます"
    )
    
    # 選択された専門家の詳細説明
    expert_details = {
        "医師": "🩺 **医師** - 健康や医療に関する質問にお答えします。症状の相談、健康管理のアドバイス、医療情報の提供を行います。",
        "料理研究家": "👨‍🍳 **料理研究家** - 料理のレシピや調理法、食材の選び方、栄養に関するアドバイスを提供します。",
        "ITエンジニア": "💻 **ITエンジニア** - プログラミング、システム開発、技術的な問題解決について専門的なサポートを提供します。",
        "ファイナンシャルプランナー": "💰 **ファイナンシャルプランナー** - 投資、保険、資産運用、家計管理について専門的なアドバイスを提供します。"
    }
    
    st.info(expert_details[expert_type])
    
    # 入力フォーム
    st.subheader("💬 相談内容を入力してください")
    user_input = st.text_area(
        f"{expert_type}への相談内容:",
        placeholder=f"{expert_type}に相談したい内容を詳しく記入してください...",
        height=150,
        help="具体的な状況や質問を入力すると、より適切なアドバイスを受けることができます"
    )
    
    # 相談ボタンと回答表示
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 相談する", type="primary", use_container_width=True):
            if user_input.strip():
                with st.spinner(f"{expert_type}が回答を準備中..."):
                    # LLMから回答を取得
                    response = get_llm_response(user_input, expert_type)
                    
                    # 回答を表示
                    st.success("✅ 回答が完了しました！")
                    st.markdown(f"### 📝 {expert_type}からの回答")
                    st.markdown(response)
                    
            else:
                st.warning("⚠️ 相談内容を入力してください。")
    
    # サイドバー情報
    with st.sidebar:
        st.header("📊 アプリ情報")
        st.markdown(f"**現在選択中**: {expert_type}")
        
        # APIキーの設定状況確認
        if os.getenv("OPENAI_API_KEY"):
            st.success("✅ OpenAI API設定済み")
        else:
            st.error("❌ OpenAI APIキーが設定されていません")
            st.markdown("""
            **設定方法**:
            1. `.env`ファイルを作成
            2. `OPENAI_API_KEY=your_api_key`を追加
            """)
        
        st.markdown("---")
        st.markdown("""
        **使用技術**:
        - Streamlit
        - LangChain
        - OpenAI GPT-3.5-turbo
        """)

if __name__ == "__main__":
    main()
