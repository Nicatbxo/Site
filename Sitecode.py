import streamlit as st
from streamlit_autorefresh import st_autorefresh
from googleapiclient.discovery import build

# Səhifənin 5 saniyədən bir avtomatik yenilənməsi
st_autorefresh(interval=5000, key="datarefresh")

st.set_page_config(page_title="Canlı YouTube İzləmə", page_icon="📈")

st.title("📊 Canlı YouTube Analitika")

# API açarını təhlükəsizlik üçün st.secrets-dən çəkmək olar
# Amma ilkin olaraq buraya birbaşa yaza bilərsən
API_KEY = "BURA_GOOGLE_API_ACARINI_YAZ"
youtube = build("youtube", "v3", developerKey=API_KEY)

video_id = st.text_input("YouTube Video ID-sini daxil edin:", placeholder="məsələn: dQw4w9WgXcQ")

if video_id:
    try:
        request = youtube.videos().list(part="statistics,snippet", id=video_id)
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            data = response['items'][0]
            stats = data['statistics']
            title = data['snippet']['title']
            
            st.success(f"Video: {title}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Baxış", f"{int(stats['viewCount']):,}")
            col2.metric("Bəyənmə", f"{int(stats['likeCount']):,}")
            col3.metric("Rəy", f"{int(stats['commentCount']):,}")
        else:
            st.error("Video tapılmadı!")
    except Exception as e:
        st.error(f"Xəta baş verdi: {e}")
