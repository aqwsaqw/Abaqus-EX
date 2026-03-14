# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 16:04:52 2025

@author: aqwsa
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 创建一个3D图形
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# 设置椭球的参数
a = 2.0  # x轴半径
b = 1.5  # y轴半径
c = 1.0  # z轴半径

# 创建网格点
phi = np.linspace(0, 2. * np.pi, 100)
theta = np.linspace(0, np.pi, 100)
phi, theta = np.meshgrid(phi, theta)

# 计算椭球上的点坐标
x = a * np.sin(theta) * np.cos(phi)
y = b * np.sin(theta) * np.sin(phi)
z = c * np.cos(theta)

# 绘制椭球面
ax.plot_surface(
    x, y, z, rstride=5, cstride=5, color='c', edgecolors='k',
    linewidth=0.5, antialiased=True, alpha=0.8
)

# 绘制网格线
ax.plot_wireframe(x, y, z, rstride=10, cstride=10, color='k', alpha=0.3)

# 设置坐标轴标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 设置图形标题
plt.title('Ellipsoid with Grid Lines')

# 显示图形
plt.show()