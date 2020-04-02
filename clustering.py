import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# import plotly.express as px

"""## Mengambil data di drive
bisa dirubah dengan tidak menggunakan drive
"""

from google.colab import drive #mount drive
drive.mount('/content/gdrive')
path = 'gdrive/My Drive/Colab Notebooks/datasetCluster2.csv'
dataset = pd.read_csv(path)

dataset.head()

dataset.describe()

dataset.info()

sns.scatterplot(x='age', y='overall', data=dataset)

"""## Pembuatan centroid dengan K = 3"""

centro = [
    [18, 60, '0'],
    [24, 80, '1'],
    [31, 65, '2'],
]

# kita buat menjadi dataframe
centroid = pd.DataFrame(centro, columns=['age', 'overall', 'cluster'])
centroid

"""penentuan centroid awal dapat mempengaruhi hasil clustering

## Memasukkan centroid sesuai titiknya
"""

sns.scatterplot(x='age', y='overall', hue='cluster', data=dataset.append(centroid))

"""cluster -1 artinya adalah belum masuk ke dalam salah satu cluster (bisa diganti angka lain)

## Pembuatan data untuk pergantian centroid
"""

update = [
    [0, 0, '0'],
    [0, 0, '1'],
    [0, 0, '2'],
]

# kita buat menjadi dataframe
centroidBaru = pd.DataFrame(update, columns=['age', 'overall', 'cluster'])
centroidBaru

"""## Proses clustering dan perubahan titik centroid
dilakukan hingga posisi titik centroid sudah tidak berpindah lagi
"""

notSame = True
j = 1
while (notSame is True): #akan melakukan looping selama "notSame " bernilai True (titik centroid sudah tidak berubah)
    clusterr = []
    baru  = []

    x02, y02 = centroid.iloc[0][['age', 'overall']] #mengambil titik Centroid ke 0
    x12, y12 = centroid.iloc[1][['age', 'overall']] #mengambil titik Centroid ke 1
    x22, y22 = centroid.iloc[2][['age', 'overall']] #mengambil titik Centroid ke 2

    #mencari centroid terdekat dengan setiap titik
    for i in range(len(dataset)):
        x1, y1 = dataset.iloc[i][['age', 'overall']] #mengambil titik untuk setiap data pada dataset

        # euclidean distant
        dist0 = ((x02-x1)**2 + (y02-y1)**2)**0.5 
        dist1 = ((x12-x1)**2 + (y12-y1)**2)**0.5
        dist2 = ((x22-x1)**2 + (y22-y1)**2)**0.5

        if (dist0 < dist1) and (dist0 < dist2): #jika nilai dist0 paling kecil, cluster = 0
            hasil = '0'
        elif  (dist1 < dist0) and (dist1 < dist2): #jika nilai dist1 paling kecil, cluster = 1
            hasil = '1'
        elif  (dist2 < dist0) and (dist2 < dist1): #jika nilai dist2 paling kecil, cluster = 2
            hasil = '2'
        clusterr.append(hasil) #append hadil cluster tadi ke list clusterr

    dataset['cluster'] = clusterr #ganti kolom 'cluster' pada dataset dengan list clusterr tadi
    
    #Update centroid
    x0 = dataset[dataset['cluster'] == '0']['age'].tolist() #mengambil semua nilai pada kolom 'age' yang cluster nya 0
    y0 = dataset[dataset['cluster'] == '0']['overall'].tolist() #mengambil semua nilai pada kolom 'overall' yang cluster nya 0
    
    #menghitung mean untuk nilai baru dari centroid 0
    mean_x0 = sum(x0) / len(x0) 
    mean_y0 = sum(y0) / len(y0)

    x1 = dataset[dataset['cluster'] == '1']['age'].tolist() #mengambil semua nilai pada kolom 'age' yang cluster nya 1
    y1 = dataset[dataset['cluster'] == '1']['overall'].tolist() #mengambil semua nilai pada kolom 'overall' yang cluster nya 1
    
    #menghitung mean untuk nilai baru dari centroid 1
    mean_x1 = sum(x1) / len(x1)
    mean_y1 = sum(y1) / len(y1)

    x2 = dataset[dataset['cluster'] == '2']['age'].tolist() #mengambil semua nilai pada kolom 'age' yang cluster nya 2
    y2 = dataset[dataset['cluster'] == '2']['overall'].tolist() #mengambil semua nilai pada kolom 'overall' yang cluster nya 2
    
    #menghitung mean untuk nilai baru dari centroid 2
    mean_x2 = sum(x2) / len(x2)
    mean_y2 = sum(y2) / len(y2)

    #mengganti nilai centroidBaru dengan mean yang sudah dihitung tadi
    centroidBaru.iloc[0,0] = mean_x0
    centroidBaru.iloc[0,1] = mean_y0
    centroidBaru.iloc[1,0] = mean_x1
    centroidBaru.iloc[1,1] = mean_y1
    centroidBaru.iloc[2,0] = mean_x2
    centroidBaru.iloc[2,1] = mean_y2

    if (centroidBaru.iloc[0,:2].all() != centroid.iloc[0,:2].all()): #jika kolom age dan overall pada centroidBaru dan centroid beda (centroid berpindah)
        #mengganti nilai centroid dengan centroidBaru dan mengganti nilai centroidBaru (disini saya hanya menukar nilai centroid dan centroidBaru)
        centroid,centroidBaru = centroidBaru, centroid 
    else: #jika centroid dan centroidBaru sama (centroid tidak berpindah)
        notSame = False #notSame berubah jadi False agar loop berhenti
    # print('ini loop ke ', j)
    # j = j+1

centroidBaru

"""titik centroidnya sekarang seperti ini

## Hasil Clustering
"""

sns.scatterplot(x='age', y='overall', hue='cluster', data=dataset.append(centroid))