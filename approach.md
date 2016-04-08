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
