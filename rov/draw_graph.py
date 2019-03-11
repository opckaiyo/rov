import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# CSVからデータを読み込む
data = pd.read_csv('sample.csv', delim_whitespace=True, header=0)

# 3Dグラフの初期化
fig = plt.figure()
ax = fig.gca(projection='3d')

# データの準備
Xgrid = data.columns.values.astype(np.float32)
Ygrid = data.index.values.astype(np.float32)
X, Y = np.meshgrid(Xgrid, Ygrid)
Z = data.as_matrix()

# プロット
surf = ax.plot_surface(X, Y, Z)

# 必要な場合はここでその他の設定をします。

# 表示
plt.show()
