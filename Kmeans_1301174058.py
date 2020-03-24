#!/usr/bin/env python
# coding: utf-8

# In[51]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[52]:


get_ipython().run_line_magic('matplotlib', 'inline')
data = pd.DataFrame ({
    'x': [20,15,60,33,55,8,10,50,44,5],
    'y': [52,50,22,16,38,25,47,36,20,6]
})

np.random.seed(200)
k = 3
centroids = {
    i+1: [np.random.randint(0, 70), np.random.randint(0, 70)]
    for i in range(k)
}

fig = plt.figure(figsize=(5, 5))
plt.scatter(data['x'], data['y'], color='k')
colmap = {1: 'r', 2: 'y', 3: 'b'}
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i])
plt.xlim(0,70)
plt.ylim(0,70)
plt.show()


# In[53]:


def assign(data, centroids):
    for i in centroids.keys():
        data['distance_from_{}'.format(i)] = (
            np.sqrt(
                (data['x'] - centroids[i][0]) ** 2 + (data['y'] - centroids[i][1]) ** 2
            )
        )
    centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
    data['closest'] = data.loc[:, centroid_distance_cols].idxmin(axis=1)
    data['closest'] = data['closest'].map(lambda x: int(x.lstrip('distance_from_')))
    data['color'] = data['closest'].map(lambda x: colmap[x])
    return data

data = assign(data, centroids)
print(data)

fig = plt.figure(figsize=(5, 5))
plt.scatter(data['x'], data['y'], color= data['color'], alpha=0.5, edgecolor='k')
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i])
plt.xlim(0,70)
plt.ylim(0,70)
plt.show()


# In[54]:


import copy

old_centroids = copy.deepcopy(centroids)

def update(k):
    for i in centroids.keys():
        centroids[i][0] = np.mean(data[data['closest'] == i]['x'])
        centroids[i][1] = np.mean(data[data['closest'] == i]['y'])
    return k

centroids = update(centroids)

fig = plt.figure(figsize=(5, 5))
ax = plt.axes()
plt.scatter(data['x'], data['y'], color= data['color'], alpha = 0.5, edgecolor = 'k')
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i])
plt.xlim(0,70)
plt.ylim(0,70)
for i in old_centroids.keys():
    old_x = old_centroids[i][0]
    old_y = old_centroids[i][1]
    dx = (centroids[i][0] - old_centroids[i][0]) * 0.75
    dy = (centroids[i][1] - old_centroids[i][1]) * 0.75
    ax.arrow(old_x, old_y, dx, dy, head_width=2, head_length=3, fc=colmap[i], ec=colmap[i])
plt.show()


# In[55]:


data = assign(data, centroids)

fig = plt.figure(figsize=(5, 5))
ax = plt.axes()
plt.scatter(data['x'], data['y'], color= data['color'], alpha = 0.5, edgecolor = 'k')
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i])
plt.xlim(0,70)
plt.ylim(0,70)
plt.show()


# In[56]:


while True:
    closest_centroids = data['closest'].copy(deep=True)
    centroids = update(centroids)
    data = assign(data, centroids)
    if closest_centroids.equals(data['closest']):
        break

fig = plt.figure(figsize=(5, 5))
ax = plt.axes()
plt.scatter(data['x'], data['y'], color= data['color'], alpha = 0.5, edgecolor = 'k')
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i])
plt.xlim(0,70)
plt.ylim(0,70)
plt.show()

