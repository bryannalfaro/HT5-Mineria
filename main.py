#Universidad del Valle de Guatemala
#Mineria de Datos
#HT5 Naive
#Integrantes
#Bryann Alfaro
#Diego de Jesus
#Julio Herrera

'''
Referencias
Material brindado en clase
'''

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, mean_squared_error, r2_score, silhouette_score
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.decomposition import PCA
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split
import pyclustertend
import random
from sklearn.cluster import KMeans
from sklearn import preprocessing, tree
import graphviz
import sklearn.mixture as mixture
import scipy.cluster.hierarchy as sch
from copy import copy
import matplotlib.cm as cm
from sklearn.model_selection import train_test_split
from scipy.stats import normaltest
from sklearn.linear_model import Ridge
from yellowbrick.regressor import ResidualsPlot
from statsmodels.graphics.gofplots import qqplot
import statsmodels.api as sm
import warnings
import seaborn as sn
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score ,precision_score,recall_score,f1_score
from pandas.core.common import SettingWithCopyWarning
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
houses = pd.read_csv('train.csv', encoding='latin1', engine='python')

'''
#Conocimiento de datos
print(houses.head())

#Cantidad de observaciones y variables en la base
print(houses.shape)

#Medidas estadisticas.
print(houses.describe().transpose())

print(houses.select_dtypes(exclude=['object']).info())'''

'''#Casas que ofrecen todas las utilidades
print(houses['Utilities'].value_counts())

plt.bar(houses['Utilities'].value_counts().sort_index().dropna().index, houses['Utilities'].value_counts().sort_index().values, color='red')
plt.title('Grafico de barras para utilidades')
plt.xlabel('Utilidad')
plt.xticks(rotation=90)
plt.ylabel('Cantidad de casas')
plt.tight_layout()
plt.show()

#Calidad de casas predominante
print(houses['OverallCond'].value_counts())

plt.bar(houses['OverallCond'].value_counts().sort_index().dropna().index, houses['OverallCond'].value_counts().sort_index().values, color='red')
plt.title('Grafico de barras para condicion de las casas')
plt.xlabel('Condicion')
plt.ylabel('Cantidad de casas')
plt.show()

#A??o de mas y menos produccion de casas para
print(houses['YearBuilt'].value_counts().sort_values(ascending=False).head(1))
print(houses['YearBuilt'].value_counts().sort_values(ascending=True).head(15))

#Capacidad de carros de las 5 casas mas caras y baratas

print(houses.sort_values(by='SalePrice', ascending=False)[['GarageCars','SalePrice']].head(5))
print(houses.sort_values(by='SalePrice', ascending=True)[['GarageCars','SalePrice']].head(5))

#Condicion de garage y calidad de la cocina de las 5 casas mas caras
print(houses.sort_values(by='SalePrice', ascending=False)[['GarageCond','KitchenQual','SalePrice']].head(5))'''

houses_clean = houses.select_dtypes(exclude='object').drop('Id', axis=1)

'''#preprocesamiento
corr_data = houses_clean.iloc[:,:]
mat_correlation=corr_data.corr() # se calcula la matriz , usando el coeficiente de correlacion de Pearson
plt.figure(figsize=(16,10))

#Realizando una mejor visualizacion de la matriz
sns.heatmap(mat_correlation,annot=True,cmap='BrBG')
plt.title('Matriz de correlaciones  para la base Houses')
plt.tight_layout()
plt.show()'''

# Seleccion de variables
houses_df = houses_clean[['OverallQual', 'OverallCond', 'GrLivArea', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'TotalBsmtSF', '1stFlrSF', 'FullBath', 'Fireplaces',
'GarageCars', 'GarageArea', 'GarageYrBlt','TotRmsAbvGrd','SalePrice']]
'''
print(houses_df.head().dropna())
print(houses_df.info())
print(houses_df.describe().transpose())
'''
houses_df.fillna(0)

#normalizar
df_norm  = (houses_df-houses_df.min())/(houses_df.max()-houses_df.min())
#print(movies_clean_norm.fillna(0))
houses_df_final = df_norm.fillna(0)

'''#Analisis de tendencia a agrupamiento

#Metodo Hopkings

random.seed(200)
print(pyclustertend.hopkins(houses_df_final, len(houses_df_final)))

#Grafico VAT e iVAT
x = houses_df_final.sample(frac=0.1)
pyclustertend.vat(x)
plt.show()
pyclustertend.ivat(x)
plt.show()

# Numero adecuado de grupos
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, max_iter=300)
    kmeans.fit(houses_df_final)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('Grafico de codo')
plt.xlabel('No. Clusters')
plt.ylabel('Puntaje')
plt.show()

#Kmeans
clusters=  KMeans(n_clusters=3, max_iter=300) #Creacion del modelo
clusters.fit(houses_df_final) #Aplicacion del modelo de cluster

houses_df_final['cluster'] = clusters.labels_ #Asignacion de los clusters
print(houses_df_final.head())

pca = PCA(2)
pca_movies = pca.fit_transform(houses_df_final)
pca_movies_df = pd.DataFrame(data = pca_movies, columns = ['PC1', 'PC2'])
pca_clust_movies = pd.concat([pca_movies_df, houses_df_final[['cluster']]], axis = 1)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('PC1', fontsize = 15)
ax.set_ylabel('PC2', fontsize = 15)
ax.set_title('Clusters de casas', fontsize = 20)

color_theme = np.array(['red', 'green', 'blue', 'yellow','black'])
ax.scatter(x = pca_clust_movies.PC1, y = pca_clust_movies.PC2, s = 50, c = color_theme[pca_clust_movies.cluster])

plt.show()
print(pca_clust_movies)

houses_df['Cluster'] = houses_df_final['cluster']
print((houses_df[houses_df['Cluster']==0]).describe().transpose())
print((houses_df[houses_df['Cluster']==1]).describe().transpose())
print((houses_df[houses_df['Cluster']==2]).describe().transpose())
houses_df.pop('Cluster)
'''

# Creacion de la respuesta (clasificacion de casas en: Economicas, Intermedias o Caras)
minSalesPrice = houses_df['SalePrice'].min()
maxSalesPrice = houses_df['SalePrice'].max()
terceraParte = (maxSalesPrice - minSalesPrice) / 3
houses_df['Clasificacion'] = houses_df['SalePrice']
# Clasificar casas a partir del precio "SalePrice"
houses_df['Clasificacion'] = houses_df['Clasificacion'].apply(lambda x: 'Economicas' if x < minSalesPrice + terceraParte else 'Intermedias' if x < minSalesPrice + 2 * terceraParte else 'Caras')
# Clasificar casas a partir del precio y su condici??n general "OverallCond"
houses_df['Clasificacion'] = houses_df.apply(lambda row: 'Caras' if ((row['Clasificacion'] == 'Intermedias' and row['OverallCond'] < 4 ) or (row['Clasificacion'] == 'Economicas' and row['OverallCond'] < 2))
                                                    else 'Intermedias' if (row['Clasificacion'] == 'Economicas' and (1 < row['OverallCond'] < 4))
                                                    else 'Economicas' if (row['Clasificacion'] == 'Intermedias' and row['OverallCond'] > 7)
                                                    else row['Clasificacion'], axis=1)
# Convertir Clasaficacion a categorica
houses_df['Clasificacion'] = houses_df.apply(lambda row: 1 if row['Clasificacion'] == 'Economicas' else 2 if row['Clasificacion'] == 'Intermedias' else 3, axis=1)
'''
# Ver distribucion del precio, condicion general y clasificacion
houses_df['SalePrice'].hist()
plt.title('Histograma de precios')
plt.show()
houses_df['OverallCond'].hist()
plt.title('Histograma de condicion general')
plt.show()
houses_df['Clasificacion'].hist()
plt.title('Histograma de clasificacion')
plt.show()
'''
# Division de datos, 70% de entrenamiento y 30% de prueba, manteniendo distribucion de clasificacion
y = houses_df.pop('Clasificacion')
x = houses_df
x.pop('MasVnrArea')
x.pop('GarageYrBlt')

np.random.seed(200)

x_train_reg, x_test_reg, y_train_reg, y_test_reg = train_test_split(x, y, test_size=0.3, train_size=0.7, random_state=0)

print(f'x_train_reg: {x_train_reg.shape}')
print(f'x_test_reg: {x_test_reg.shape}')
print(f'y_train_reg: {y_train_reg.shape}')
print(f'y_test_reg: {y_test_reg.shape}')

# Creacion del modelo de bayes ingenuo (Naive Bayes)

gaussian = GaussianNB()
gaussian.fit(x_train_reg, y_train_reg)

#Utilizando datos de entrenamiento
y_pred_train = gaussian.predict(x_train_reg)

# Dt_model = tree.DecisionTreeClassifier(random_state=0)

# Dt_model.fit(x_train_reg, y_train_reg)

# y_pred_train = Dt_model.predict(x_train_reg)


accuracy=accuracy_score(y_train_reg,y_pred_train)
precision =precision_score(y_train_reg, y_pred_train,average='weighted')
recall =  recall_score(y_train_reg, y_pred_train,average='weighted')
f1 = f1_score(y_train_reg,y_pred_train,average='weighted')
# print('Decision Tree Accuracy: ',accuracy)
# print('Decision Tree Accuracy: ',precision)
# print('Decision Tree Accuracy: ',recall)
print('\nAccuracy: ',accuracy)
print('Precision: ',precision)
print('Recall: ',recall)

cm = confusion_matrix(y_train_reg,y_pred_train)
sn.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Econ??micas', 'Intermedias', 'Caras'], yticklabels=['Econ??micas', 'Intermedias', 'Caras'])
plt.title('Matriz de Confusion')
plt.ylabel('Clasificaci??n real')
plt.xlabel('Clasificaci??n predicha')
plt.show()
print('\nMatriz de confusion con valores de entrenamiento \n',cm)

# Mostrando la variable categorica "Clasificacion" en conjuntos y prediccion
print('\nClasificacion en conjuntos de entrenamiento\n',y_train_reg)
print('\nClasificacion predicha en conjuntos de entrenamiento\n',y_pred_train)
print('tama??o de conjunto predicho: ',len(y_pred_train))


#Utilizando datos de prueba
# y_pred = Dt_model.predict(x_test_reg)
# Utilizando datos de prueba. Eficiencia del modelo
y_pred = gaussian.predict(x_test_reg)
accuracy=accuracy_score(y_test_reg,y_pred)
precision =precision_score(y_test_reg, y_pred,average='weighted')
recall =  recall_score(y_test_reg, y_pred,average='weighted')
f1 = f1_score(y_test_reg,y_pred,average='weighted')
print('\nAccuracy: ',accuracy)
print('Precision: ',precision)
print('Recall: ',recall)

cm = confusion_matrix(y_test_reg,y_pred)
sn.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Econ??micas', 'Intermedias', 'Caras'], yticklabels=['Econ??micas', 'Intermedias', 'Caras'])
plt.title('Matriz de Confusion')
plt.ylabel('Clasificaci??n real')
plt.xlabel('Clasificaci??n predicha')
plt.show()
print('\nMatriz de confusion con valores de test\n',cm)

# Validacion cruzada

# validacion cruzada repetida (15 conjuntos en total)
rkf = RepeatedKFold(n_splits=3, n_repeats=5, random_state=0)

# eficiencia con la validacion cruzada repetida
cv_scores = cross_val_score(gaussian, x, y, scoring='accuracy', cv=rkf)
print("\n%0.5f de accuracy con una desviacion estandar de %0.5f" % (cv_scores.mean(), cv_scores.std()))

print()
