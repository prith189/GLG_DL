# GLG_DL

 - The following pretrained files need to be downloaded before running main.py
 - The script should output a Topic, and associated keywords for each sample text provided in main.py
 
Download link for dim_red_embeddings
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1OieSf2kPtyTYuTiYJSTsNa7jpCsaQnum' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1OieSf2kPtyTYuTiYJSTsNa7jpCsaQnum" -O all-the-news-embeddings-title-umap.npy && rm -rf /tmp/cookies.txt
        
Download link for umap_model_file
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1ibBI4BMS6zKfjPWarxdNKNvOuIt5Mj2D' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1ibBI4BMS6zKfjPWarxdNKNvOuIt5Mj2D" -O umap-model.sav && rm -rf /tmp/cookies.txt

Download link for kmeans_model
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1qBL6k2w06IbXs1h_tNJb52QW6gkKhBGy' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1qBL6k2w06IbXs1h_tNJb52QW6gkKhBGy" -O kmeans_model.p && rm -rf /tmp/cookies.txt
        
Download link for labels_file
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1bNF2rhe2rdG7zzPoay_NziXAjLtwLXhg' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1bNF2rhe2rdG7zzPoay_NziXAjLtwLXhg" -O umap-kmeans-labels.npy && rm -rf /tmp/cookies.txt

Download link for topics_file
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-1LXRgomfpqloQEvbDgfR_Hx7SAnOfWD' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-1LXRgomfpqloQEvbDgfR_Hx7SAnOfWD" -O umap-kmeans-topics.p && rm -rf /tmp/cookies.txt
        

Download link for topic_labels_file
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-3p3vZYdY8iytnDn5gUaUVcabKfkrUhq' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-3p3vZYdY8iytnDn5gUaUVcabKfkrUhq" -O umap-kmeans-topic-labels.p && rm -rf /tmp/cookies.txt
        
        
