# Approach

Background: It is generally accepted that sub-genres of metal exist.

Hypothesis: If subgenres exist, groups of similar bands should be discoverable
through unsupervized learning or other exploratory methods.

## Processing

Raw data:

| Band Name & Link | Genre Descriptor | Country of Origin | Status |

Transform into:

| Band Name | Genre Descriptor | Tokenized Genre Terms | ... |

Convert tokenized genre terms into a feature vector, where each column is a 
unique term and each row is a binary representation of the tokenized genre
terms. Take for example the genre descriptor "Melodic Death Metal", which
becomes `('Melodic', 'Death', 'Metal')` upon tokenization, and then can be
binarized like so:

| Metal | Death | Black | Doom | Melodic | ... |
| 1     | 1     | 0     | 0    | 1       | ... |

Now we have a feature vector representing the genre data for a given band.

The term 'Metal' appears in almost every genre descriptor, so it is omitted
from the binarized feature vector.

### Challenges to processing

Cannot run `sklearn.preprocessing.MultiLabelBinarizer` on entire data set at
once because `numpy` returns a `MemoryError`. I may need to use a swapfile.
Other alternatives: batch processing in groups of 1000. `MultiLabelBinarizer`
works with 2000 entries, fails with 5000, haven't tried anything in between.

## Exploration

### Multi-Dimensional Scaling (MDS)

Visualizing results shows a plot of distinct concentric circles. Suggests some
kind of structure exists in the data set.

### Principal Component Analysis (PCA)

Visualizing first two principal components reveals six distinct groups.
Running K-Means clustering with K = 6 effectively assigns each point to a
centroid. Re-visualizing the MDS results, this time coloring points according
to K-Means cluster membership reveals each cluster as a wedge of the concentric
circles.

To visualize:
* Additional PCA components past 1 and 2
* MDS results, concentric circle ~~significance unclear~~ structure signifies number
of genre descriptor terms
	* Color by distance from K-means centroid -> unclear if this matters
	* Color by number of tokenized terms -> corresponds with concentric circles

### Clustering on PCA results

#### K-means
Quick, but only finds spherical clusters. PCA results show non-circular
clusters of different shapes and sizes.

#### DBSCAN
DBSCAN detects clusters based on point density. It takes a distance parameter
$\epsilon$ (between points) and a minimum number of points (4-5 for 2D data)
that defines a single cluster. It is capable of detecting clusters that are
non-spherical in shape and clusters of different sizes.

If we choose `min_points = 5` (`sklearn` default), then finding $\epsilon$
requires we make a histogram of the distances to the 5th nearest point for all
points in the data set. To make this histogram, use the
`sklearn.neighbors.KDTree` class. Most points should lie below a distance from
each other. Just above this value should be a good choice for $\epsilon$.

### Network analysis

Nodes: Bands

Edges: Overlapping genre terms

#### Visualization options

##### Graph / NetworkX

Graph definitions

* Bands
	* Nodes: Bands
	* Edges: Overlapping genre terms

* Genre descriptors
	* Nodes: Unique Genre descriptors, sized by number (of bands)
	* Edges: Overlapping genre terms


Visualization approaches

1. Edge emphasis: color by overlap term for top N genre terms

2. Node emphasis: color nodes by K-means/DBSCAN cluster membership

##### Word Cloud

1. Word cloud for each cluster / country

##### Breakdowns

* By country - Interesting, but might be too verbose (how do we pick which
countries?)
* By K-means/DBSCAN cluster membership - Potentially interesting, possibly
redundant
* By status - Fewer overall visualizations, still interesting. Can see what
used to be popular.
