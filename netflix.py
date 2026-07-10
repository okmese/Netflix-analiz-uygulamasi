import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import plotly.express as px

movie = pd.read_csv("movie.csv",parse_dates = ["date_added"])
series = pd.read_csv("series.csv",parse_dates = ["date_added"])
netflix1 = pd.concat([series , movie])
netflix = netflix1.drop(["budget","revenue","duration","vote_average"], axis = 1) 
netflix["type"] = netflix["type"].str.replace(" ", "_")

ss = st.session_state
if "analiz" not in ss:
    ss.analiz = False
if "genelAnaliz" not in ss:
    ss.genelAnaliz = False

st.markdown(
    """
    <div style="
        background-color: #84A59D; 
        padding: 25px; 
        border-radius: 12px; 
        border-right: 5px solid #FFD580; 
        box-shadow: 2px 4px 10px #84A59D ;
        margin-top: 20px;
        margin-bottom: 20px;
    ">
        <h3 style="color: #FFD580; "> 📦Netflix Analiz Uygulaması  </h3>
        <p style="color: white ; font-size: 16px;">
        Genel analiz ve Grafiksel analiz yapmak için <strong>sol üstteki kontrol panelini (sidebar)</strong> kullanarak istediğiniz grafiklere ve verilere kendi filtrelemelerinizle ulaşacaksınız.</p>

    </div>
    <style>
    span[data-baseweb="tag"]{
        background-color: #84A59D;
        color: white ;
    }
    button[kind="pillsActive"] {
        background-color: #84A59D;
        border-color: white;
        color: white;
    }
    div.stButton > button[kind="secondary"]{
        background-color:#84A59D;
        color:white;
    }

    h3,h3 span{color: #FFD580
    }
    </style>

    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns([2,1])

with col1:
    with st.container(border = True):
        " ### 📋 Veri Önizleme"
        st.dataframe(netflix.head())

with col2:
    with st.container(border = True , height = 314):
        st.subheader("📊 İstatistik")
        st.metric("Toplam Satır", len(netflix))
        st.metric("Toplam Sütun", len(netflix.columns))


st.sidebar.title("Netflix Analizi")
st.sidebar.text("Bir analiz seçin")
if st.sidebar.button("Genel Analiz"):
    ss.analiz = False
    ss.genelAnaliz = True
    with st.spinner("Genel Analiziniz yükleniyor..."):
        time.sleep(2.5)
if st.sidebar.button("Grafiksel Analiz"):
    ss.analiz = True
    ss.genelAnaliz = False
    with st.spinner("Grafiksel Analiziniz yükleniyor..."):
        time.sleep(2.5)

if ss.genelAnaliz:
    with st.container(border = True , height = 1000):
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border = True):
                st.metric(label = "Toplam İçerik Sayısı" ,value = f"{len(netflix)}")
        with col2:
            with st.container(border = True):
                st.metric(label = "Dizi Sayısı" ,value = f"{len(netflix[netflix["type"] == "TV_Show"])}")
        with col3:
            with st.container(border = True):
                st.metric(label = "Film Sayısı" ,value = f"{len(netflix[netflix["type"] == "Movie"])}")

        with st.container(border = True ):
            "# 🔥TOP 10:"
            col1, col2 = st.columns(2)
            with col1:
                ""
                ""
                ""
                ""
                "### En çok içerik üreten ülkeler:"
                ülkeÇok = netflix["country"].value_counts().head(10).reset_index()
                ülkeÇok.columns = ["Ülke", "Toplam Dizi ve Film sayısı"]
                st.dataframe(ülkeÇok ,hide_index=True,column_config={"Ülke": st.column_config.TextColumn(width= "small")})
            with col2:
                "### En çok DİZİ üreten ülkeler:"
                diziFiltre = netflix[netflix["type"] == "TV_Show"]
                diziÇok = diziFiltre["country"].value_counts().head(10).reset_index()
                diziÇok.columns = ["Ülke", "Toplam Dizi sayısı"]
                st.dataframe(diziÇok ,hide_index=True, height = 200)
                "### En çok FİLM üreten 10 Ülke:"
                filmFiltre = netflix[netflix["type"] == "Movie"]
                filmÇok = filmFiltre["country"].value_counts().head(10).reset_index()
                filmÇok.columns = ["Ülke", "Toplam Film sayısı"]
                st.dataframe(filmÇok ,hide_index=True , height = 200 ,column_config={"Ülke": st.column_config.TextColumn(width= "small")})
            ""
            "---"
            "## ✨Rating Sıralaması (ilk 100):"
            ""
            ""
            st.markdown("<h3 style='text-align: center;'>ÜLKELER</h3>", unsafe_allow_html=True)
            sıralama = netflix.groupby("country")["rating"].mean()
            st.dataframe(sıralama.sort_values(ascending = False).head(100))
            ""
            col1, col2 =st.columns(2)
            with col1: 
                st.markdown("<h3 style='text-align: center;'>DİZİLER</h3>", unsafe_allow_html=True)
                diziRating = netflix[netflix["type"] == "TV_Show"]
                diziRatingFiltre = diziRating.groupby("title")["rating"].mean()
                st.dataframe(diziRatingFiltre.sort_values(ascending = False).head(100) , height =320)

                st.markdown("<h3 style='text-align: center;'>TÜRLER</h3>", unsafe_allow_html=True)
                türRating = netflix.groupby("genres")["rating"].mean().reset_index()
                st.dataframe(türRating.sort_values(by="rating",ascending = False).head(100),hide_index=True , column_config={"genres": st.column_config.TextColumn(width= "medium")} , height =320)

            with col2:
                st.markdown("<h3 style='text-align: center;'>FİLMLER</h3>", unsafe_allow_html=True)
                filmRating = netflix[netflix["type"] == "Movie"]
                filmRatingFiltre = filmRating.groupby("title")["rating"].mean()
                st.dataframe(filmRatingFiltre.sort_values(ascending = False).head(100) , height =320)

                st.markdown("<h3 style='text-align: center;'>YILLAR</h3>", unsafe_allow_html=True)
                yılRating = netflix.groupby("release_year")["rating"].mean()
                st.dataframe(yılRating.sort_values(ascending = False).head(100) , height =320)

            ""
            "---"
            ""
            "## 🔎Veri Görme Sistemi"
            seçenek = ["TV_Show","Movie"]
            dizi_film = st.pills("Bir veya daha fazlasını seç.", seçenek, selection_mode="multi",  key = "seçenek")


            seçtiğinÜlke = st.multiselect(
                "Hangi Ülkenin verisini görmek istersin?",
                (netflix["country"].unique().dropna()), key = "multiselect"
            )                                                                                 
            başlangıç, bitiş = st.select_slider(
                "Hangi Tarih aralığında olsun?",
             options = sorted(netflix["release_year"].dropna().unique()),
                value = [2010,2020], key= "options"
            )

            seçenekAnaliz = netflix[(netflix["country"].isin(seçtiğinÜlke)) & (netflix["release_year"] >= başlangıç) & (netflix["release_year"] <= bitiş) & (netflix["type"].isin(dizi_film))]
            with st.container(border = True, height = 450):
                if not seçenekAnaliz.empty:
                    st.write(seçenekAnaliz)


if ss.analiz:
    with st.container(border = True , height = 600):
        st.sidebar.write(" ### Kontrol paneli :")

        Xdeğeri = netflix.columns.drop(["show_id","genres","description","date_added","release_year","rating","vote_count", "cast" , "popularity"])
        Ydeğeri = netflix.columns.drop(["show_id","title","genres","description","type","cast","country"])
        grafikler = ["Bar Grafiği","Çizgi Grafiği","Turta Grafiği","Donut Grafiği","Boxplot","Heatmap","Dünya Haritası Grafiği","Balon Grafiği","Alan Grafiği"]
        Xdeğeri2 = "release_year"
        Xdeğeri3 = "country"
        SeçilenGrafik = st.sidebar.selectbox("Grafik Türü",grafikler , key="secilen_grafik")


        if ss.secilen_grafik == grafikler[0]:
            Ydeğeri = Ydeğeri.drop(["date_added"])
            SeçilenX = st.sidebar.selectbox("Bar Grafiğinin X değeri:", Xdeğeri, key = "x")
            SeçilenY = st.sidebar.selectbox("Bar Grafiğinin Y değeri:", Ydeğeri, key = "y")
            grafikTürü = "bar"
        if ss.secilen_grafik == grafikler[1]:
            SeçilenX = st.sidebar.selectbox("Çizgi Grafiğinin X değeri:", Xdeğeri, key = "x")
            SeçilenY = st.sidebar.selectbox("Çizgi Grafiğinin Y değeri:", Ydeğeri, key = "y")
            grafikTürü = "line"
        if ss.secilen_grafik == grafikler[2]:
            Ydeğeri = Ydeğeri.drop(["language","director","date_added","release_year"])
            SeçilenX = st.sidebar.selectbox("Turta Grafiğinin X değeri:", Xdeğeri, key = "x")
            SeçilenY = st.sidebar.selectbox("Turta Grafiğinin Y değeri:", Ydeğeri, key = "y")
            grafikTürü = "turta"
        if ss.secilen_grafik == grafikler[3]:
            Ydeğeri = Ydeğeri.drop(["language","director","date_added","release_year"])
            SeçilenX = st.sidebar.selectbox("Donut Grafiğinin X değeri:", Xdeğeri, key = "x")
            SeçilenY = st.sidebar.selectbox("Donut Grafiğinin Y değeri:", Ydeğeri, key = "y")
            grafikTürü = "donut"
        if ss.secilen_grafik == grafikler[4]:
            Xdeğeri = Xdeğeri.drop(["director"])
            SeçilenX = st.sidebar.selectbox("Boxplot'un X değeri:", Xdeğeri, key = "x")
            SeçilenY = st.sidebar.selectbox("Boxplot'un Y değeri:", Ydeğeri, key = "y")
            grafikTürü = "boxplot"
        if ss.secilen_grafik == grafikler[5]:
            Ydeğeri = Ydeğeri.drop(["vote_count","language","director"])
            SeçilenX = st.sidebar.selectbox("Heatmap'in X değeri:", Xdeğeri, key = "x")
            SeçilenY = st.sidebar.selectbox("Heatmap'in Y değeri:", Ydeğeri, key = "y")
            grafikTürü = "heatmap"
        if ss.secilen_grafik == grafikler[6]:
            Ydeğeri = Ydeğeri.drop(["date_added","release_year"])
            SeçilenX = st.sidebar.selectbox("Dünya Haritası Grafiğinin X değeri:", Xdeğeri3, key = "x")
            SeçilenY = st.sidebar.selectbox("Dünya Haritası Grafiğinin Y değeri:", Ydeğeri, key = "y")
            grafikTürü = "dünya"
        if ss.secilen_grafik == grafikler[7]:
            SeçilenX = st.sidebar.selectbox("Balon Grafiğinin X değeri:", Xdeğeri, key = "x")
            SeçilenY = st.sidebar.selectbox("Balon Grafiğinin Y değeri:", Ydeğeri, key = "y")
            grafikTürü = "balon"
        if ss.secilen_grafik == grafikler[8]:
            Ydeğeri = Ydeğeri.drop(["language","director","date_added","release_year"])
            SeçilenX = st.sidebar.selectbox("Alan Grafiğinin X değeri:", Xdeğeri2, key = "x")
            SeçilenY = st.sidebar.selectbox("Alan Grafiğinin Y değeri:", Ydeğeri, key = "y")
            grafikTürü = "alan"



        if SeçilenX == SeçilenY:
            st.sidebar.info("Satır ve sütun aynı olamaz !")
        else:
            seçilenXparametre = st.multiselect(f"{SeçilenX} seçiniz: ",(netflix[SeçilenX].dropna().unique()), key = "parametreX")         
            filtre = netflix[netflix[SeçilenX].isin(seçilenXparametre)]

            if len(seçilenXparametre) > 0:

                if grafikTürü == "bar":
                    if SeçilenY in ["rating","popularity","release_year"]: 
                        sıralama = filtre.groupby(SeçilenX)[[SeçilenY]].mean().reset_index()
                        grafikÇizim = sıralama.plot(x=SeçilenX,y=SeçilenY,kind="barh",color = "#84A59D" ,alpha=0.4 )
                    elif SeçilenY in ["date_added"]:
                        st.info("Bunun için başka grafik deneyiniz! ")
                    else:
                        sıralama = filtre.groupby(SeçilenX)[[SeçilenY]].count().reset_index()
                        grafikÇizim = sıralama.plot(x=SeçilenX,y=SeçilenY,kind="barh",color = "#84A59D",alpha=0.4)

                if grafikTürü == "line":
                    if SeçilenY in ["rating","popularity","release_year","date_added"]: 
                        sıralama = filtre.groupby(SeçilenX)[[SeçilenY]].mean().reset_index()
                        grafikÇizim = sıralama.plot(x=SeçilenX,y=SeçilenY,kind="line",color = "#84A59D",alpha=0.4  )
                    else:
                        sıralama = filtre.groupby(SeçilenX)[[SeçilenY]].count().reset_index()
                        grafikÇizim = sıralama.plot(x=SeçilenX,y=SeçilenY,kind="line",color = "#84A59D",alpha=0.4)

                if grafikTürü == "turta":
                    if SeçilenY in ["rating","popularity","release_year","date_added"]: 
                        sıralama = filtre.groupby(SeçilenX)[[SeçilenY]].mean().reset_index()
                        grafikÇizim = sıralama.plot(x=SeçilenX,y=SeçilenY,kind="pie",color = "#84A59D"  )
                    else:
                        sıralama = filtre.groupby(SeçilenX)[[SeçilenY]].count().reset_index()
                        grafikÇizim = sıralama.plot(x=SeçilenX,y=SeçilenY,kind="pie",color = "#84A59D")
                    plt.legend(labels=seçilenXparametre,title=SeçilenX,loc="center left",bbox_to_anchor=(1, 0, 0.5, 1))

                if grafikTürü == "donut":
                    if SeçilenY in ["rating","popularity","release_year","date_added"]: 
                        sıralama = filtre.groupby(SeçilenX)[[SeçilenY]].mean().reset_index()
                        grafikÇizim = px.pie(sıralama ,names=SeçilenX,values=SeçilenY,color = SeçilenX ,hole = 0.5 )
                    else:
                        sıralama = filtre.groupby(SeçilenX)[[SeçilenY]].count().reset_index()
                        grafikÇizim = px.pie(sıralama,names=SeçilenX,values=SeçilenY,color = SeçilenX ,hole = 0.5)

                if grafikTürü == "balon":
                    if SeçilenY in ["rating","popularity","release_year","date_added"]: 
                        sıralama = filtre.groupby(SeçilenX)[[SeçilenY]].mean().reset_index()
                        grafikÇizim = px.scatter(filtre ,x=SeçilenX,y=SeçilenY,color = SeçilenX )
                    else:
                        sıralama = filtre.groupby(SeçilenX)[[SeçilenY]].count().reset_index()
                        grafikÇizim = px.scatter(sıralama ,x=SeçilenX,y=SeçilenY,color = SeçilenX , size=SeçilenY)

                if grafikTürü == "boxplot":
                    grafikÇizim = px.box(filtre , x=SeçilenX,y=SeçilenY )

                if grafikTürü == "heatmap":
                    grafikÇizim = px.density_heatmap(filtre , x=SeçilenX,y=SeçilenY )

                if grafikTürü == "dünya":
                    if SeçilenY in ["rating","popularity","vote_count"]:
                        sıralama = filtre.groupby(SeçilenX)[SeçilenY].mean().reset_index()
                    else:
                        sıralama = filtre.groupby(SeçilenX)[[SeçilenY]].count().reset_index()
                    grafikÇizim = px.choropleth(sıralama , locations=SeçilenX,locationmode = "country names" , color = SeçilenY ,color_continuous_scale="Mint")
                    grafikÇizim.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)',framecolor='#84A59D',projection_type="orthographic"),font=dict(color="white"),coloraxis_colorbar=dict(title_font_size = 20))

                if grafikTürü == "alan":
                    sıralama = filtre.groupby(SeçilenX)[SeçilenY].mean().reset_index()
                    grafikÇizim = px.area(sıralama , x=SeçilenX,y=SeçilenY ,color =SeçilenX)

                if grafikTürü in["bar" , "line" , "turta"]:
                    grafikÇizim.spines["top"].set_color("white")
                    grafikÇizim.spines["bottom"].set_color("white")
                    grafikÇizim.spines["right"].set_color("white")
                    grafikÇizim.spines["left"].set_color("white")

                    grafikÇizim.get_legend().get_frame().set_facecolor("None")
                    for LegendYazısı in grafikÇizim.get_legend().get_texts():
                        LegendYazısı.set_color("white")

                    grafikÇizim.tick_params(axis="x", colors="white")
                    grafikÇizim.tick_params(axis="y", colors="white")
                    grafikÇizim.set_xlabel(SeçilenX, color="#FFD580")
                    grafikÇizim.set_ylabel(SeçilenY, color="#FFD580")
                    st.pyplot(plt , transparent = True )
                else:
                    st.plotly_chart(grafikÇizim)


            else:
                st.info("Lütfen analiz etmek için yukarıdan en az bir değer seçin.")

