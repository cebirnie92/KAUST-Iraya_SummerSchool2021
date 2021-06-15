import tensorflow.keras as keras
import numpy as np
from random import shuffle



class CosineClusters():
    """Represents a set of clusters over a dataset
    
    """
    
    
    def __init__(self, num_clusters=100):
        
        self.clusters = [] # clusters for unsupervised and lightly supervised sampling
        self.item_cluster = {} # each item's cluster by the id of the item


        # Create initial clusters
        for i in range(0, num_clusters):
            self.clusters.append(Cluster())
        
        
    def add_random_training_items(self, items):
        """ Adds items randomly to clusters    
        """ 
        
        cur_index = 0
        for item in items:
            self.clusters[cur_index].add_to_cluster(item)
            docid = item[0]
            self.item_cluster[docid] = self.clusters[cur_index]
            
            cur_index += 1
            if cur_index >= len(self.clusters):
                cur_index = 0 


    def add_items_to_best_cluster(self, items):
        """ Adds multiple items to best clusters
        
        """
        added = 0
        for item in items:
            new = self.add_item_to_best_cluster(item)
            if new:
                added += 1
                
        return added



    def get_best_cluster(self, item):
        """ Finds the best cluster for this item
            
            returns the cluster and the score
        """
        best_cluster = None 
        best_fit = float("-inf")        
             
        for cluster in self.clusters:
            fit = cluster.cosine_similarity(item)
            if fit > best_fit:
                best_fit = fit
                best_cluster = cluster 
        
        return [best_cluster, best_fit]
    
       

    def add_item_to_best_cluster(self, item):
        """ Adds items to best fit cluster    
            
            Removes from previous cluster if it existed in one
            Returns True if item is new or moved cluster
            Returns Fales if the item remains in the same cluster
        """ 
        
        best_cluster = None 
        best_fit = float("-inf")        
        previous_cluster = None
        
        # Remove from current cluster so it isn't contributing to own match
        docid = item[0]
        if docid in self.item_cluster:
            previous_cluster = self.item_cluster[docid]
            previous_cluster.remove_from_cluster(item)
            
        for cluster in self.clusters:
            fit = cluster.cosine_similarity(item)
            if fit > best_fit:
                best_fit = fit
                best_cluster = cluster 
        
        best_cluster.add_to_cluster(item)
        self.item_cluster[docid] = best_cluster
        
        if best_cluster == previous_cluster:
            return False
        else:
            return True
 
 
    def get_items_cluster(self, item):  
        docid = item[0]
        
        if docid in self.item_cluster:
            return self.item_cluster[docid]
        else:
            return None      
        
        
    def get_centroids(self):  
        centroids = []
        for cluster in self.clusters:
            centroids.append(cluster.get_centroid())
        
        return centroids
    
        
    def get_outliers(self):  
        outliers = []
        for cluster in self.clusters:
            outliers.append(cluster.get_outlier())
        
        return outliers
 
         
    def get_randoms(self, number_per_cluster, verbose=False):  
        randoms = []
        for cluster in self.clusters:
            randoms += cluster.get_random_members(number_per_cluster, verbose)
        
        return randoms
   
      
    def shape(self):  
        lengths = []
        for cluster in self.clusters:
            lengths.append(cluster.size())
        
        return str(lengths)
    
class Cluster():
    """Represents on cluster for unsupervised or lightly supervised clustering
            
    """
    
    feature_idx = {} # the index of each feature as class variable to be constant 


    def __init__(self):
        self.members = {} # dict of items by item ids in this cluster
        self.feature_vector = [] # feature vector for this cluster
    
    def add_to_cluster(self, item):
        docid = item[0]
        features = item[1]
        
        self.members[docid] = item
        for feature in features:
            while len(self.feature_vector) <= feature:
                self.feature_vector.append(0)
            
            self.feature_vector[feature] +=1
    
        
            
    def remove_from_cluster(self, item):
        """ Removes if exists in the cluster        
            
        """
        docid = item[0]
        features = item[1]
        
        exists = self.members.pop(docid, False)
        
        if exists:
            for feature in features:
                if feature < len(self.feature_vector):
                    self.feature_vector[feature] -=1

        
    def cosine_similarity(self, item):
        features = item[1]
#         words = text.split()  
        
        vector = [0] * len(self.feature_vector)
        for feature in features:
            while len(vector) <= feature:
                self.feature_vector.append(0)
                vector.append(0)
            vector[feature] += 1
        
        item_tensor = keras.backend.constant(np.array(vector))
        cluster_tensor = keras.backend.constant(np.array(self.feature_vector))
        
        similarity = keras.losses.cosine_similarity(item_tensor, cluster_tensor, 0)
        
        return similarity.numpy() # item() converts tensor value to float
    
    
    def size(self):
        return len(self.members.keys())
 
    def get_centroid(self):
        if len(self.members) == 0:
            return []
        
        best_item = None
        best_fit = float("-inf")
        
        for docid in self.members.keys():
            item = self.members[docid]
            similarity = self.cosine_similarity(item)
            if similarity > best_fit:
                best_fit = similarity
                best_item = item
                
        best_item[2] = "cluster_centroid"
                
        return best_item
     
         

    def get_outlier(self):
        if len(self.members) == 0:
            return []
        
        best_item = None
        biggest_outlier = float("inf")
        
        for docid in self.members.keys():
            item = self.members[docid]
            similarity = self.cosine_similarity(item)
            if similarity < biggest_outlier:
                biggest_outlier = similarity
                best_item = item

        best_item[2] = "cluster_outlier"

        return best_item



    def get_random_members(self, number=1, verbose=False):
        if len(self.members) == 0:
            return []        
        
        keys = list(self.members.keys())
        shuffle(keys)

        randoms = []
        for i in range(0, number):
            if i < len(keys):
                docid = keys[i] 
                item = self.members[docid]
                item[2] = "cluster_member"

                randoms.append(item)
         
        if verbose:
            print("\nRandomly items selected from cluster:")
            for item in randoms:
                print("\t"+item[1])         
                
        return randoms
    
def get_cluster_samples(data, num_clusters=5, max_epochs=5, limit=5000):
    """Create clusters using cosine similarity
    Creates clusters until converged or max_epochs passes over the data 

    """ 

    if limit > 0:
        shuffle(data)
        data = data[:limit]

    cosine_clusters = CosineClusters(num_clusters)

    cosine_clusters.add_random_training_items(data)

    for i in range(0, max_epochs):
        print("Epoch "+str(i))
        added = cosine_clusters.add_items_to_best_cluster(data)
        if added == 0:
            break

    centroids = cosine_clusters.get_centroids()
    outliers = cosine_clusters.get_outliers()
    randoms = cosine_clusters.get_randoms(1)

    diversity_samples = centroids + outliers+ randoms
    div_unique=[]
    for x in diversity_samples:
        if x not in div_unique:
            div_unique.append(x)

    return div_unique
